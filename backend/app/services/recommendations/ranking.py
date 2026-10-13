import json
import logging
from collections import defaultdict
from typing import Dict, List

from sqlalchemy.orm import Session

from app.core import llm_gateway
from app.core.exceptions import LLMUnavailable
from app.core.llm import invoke_with_retry
from app.models.recommendation import Content
from app.services.recommendations.schemas import RankedRecommendations
from app.services.recommendations.weights import (
    CANDIDATE_K,
    CBF_WEIGHT,
    CF_WEIGHT,
    RL_WEIGHT,
    TOP_N,
)

logger = logging.getLogger(__name__)

# The student sees this line as the run's strategy, so it has to say plainly that
# the ordering is the arithmetic one and that no item was explained.
_FALLBACK_SUMMARY = (
    "Ranked by your profile match score alone — the explanation step was unavailable, "
    "so none of these items comes with a reason for why it suits you ({reason})."
)


def _merge_and_rank(
    db: Session, cf_scores: Dict, cbf_scores: Dict,
    user_ctx: Dict, expansion_scores: Dict = None,
) -> List[Dict]:
    """
    Merges CF + CBF + expansion, applies RL exploration bonus,
    enforces content-type and topic diversity.

    RL bonus: rewards content types and topics the user hasn't explored much.
    This prevents the agent from always recommending the same format.
    """
    expansion_scores = expansion_scores or {}
    all_ids = set(cf_scores) | set(cbf_scores) | set(expansion_scores)
    if not all_ids:
        return []

    # Count seen content types (for RL exploration)
    seen_types: Dict[str, int] = defaultdict(int)
    if user_ctx["seen_content_ids"]:
        for _, ct in db.query(Content.id, Content.content_type).filter(
            Content.id.in_(user_ctx["seen_content_ids"])
        ).all():
            seen_types[ct.value] += 1

    rows = db.query(
        Content.id, Content.content_type, Content.topics, Content.language
    ).filter(Content.id.in_(list(all_ids))).all()

    cid_to_type   = {r[0]: r[1].value for r in rows}
    cid_to_topics = {r[0]: (r[2] or []) for r in rows}
    cid_to_lang   = {r[0]: (r[3] or "").lower() for r in rows}
    max_seen      = max(seen_types.values(), default=1) or 1
    pref_langs    = {lang.lower() for lang in user_ctx["preferred_languages"]}

    candidates = []
    for cid in all_ids:
        cf  = cf_scores.get(cid, 0.0)
        cbf = cbf_scores.get(cid, 0.0)
        exp = expansion_scores.get(cid, 0.0)
        ct  = cid_to_type.get(cid, "article")

        # RL: reward under-explored content types
        rl = RL_WEIGHT * (1.0 - seen_types.get(ct, 0) / max_seen)

        # Language bonus
        lang_bonus = 0.05 if cid_to_lang.get(cid, "") in pref_langs else 0.0

        effective_cbf = max(cbf, exp)
        blended = round(
            min(CF_WEIGHT * cf + CBF_WEIGHT * effective_cbf + rl + lang_bonus, 1.0), 4
        )

        candidates.append({
            "content_id":    cid,
            "cf_score":      round(cf, 4),
            "cbf_score":     round(effective_cbf, 4),
            "rl_bonus":      round(rl, 4),
            "blended_score": blended,
            "content_type":  ct,
            "topics":        cid_to_topics.get(cid, []),
            "is_expansion":  cid in expansion_scores and cid not in cbf_scores,
        })

    candidates.sort(key=lambda x: x["blended_score"], reverse=True)

    # Diversity enforcement: max 3 per content_type, max 2 per primary topic
    type_count:  Dict[str, int] = defaultdict(int)
    topic_count: Dict[str, int] = defaultdict(int)
    diverse, overflow = [], []

    for c in candidates:
        ct    = c["content_type"]
        ptopic = (c["topics"][0] if c["topics"] else "general").lower()
        if type_count[ct] < 3 and topic_count[ptopic] < 2:
            diverse.append(c)
            type_count[ct] += 1
            topic_count[ptopic] += 1
        else:
            overflow.append(c)
        if len(diverse) >= CANDIDATE_K:
            break

    if len(diverse) < CANDIDATE_K:
        diverse.extend(overflow[:CANDIDATE_K - len(diverse)])

    return diverse


def _score_ordered(candidates: List[Dict], reason: str) -> Dict:
    fallback_ids = [c["content_id"] for c in candidates[:TOP_N]]
    return {
        "ranked_ids":   fallback_ids,
        "explanations": {str(cid): "" for cid in fallback_ids},
        "summary":      _FALLBACK_SUMMARY.format(reason=reason),
        "tokens_used":  0,
        "model_used":   "fallback",
    }


def rank_with_llm(
    db: Session, user_ctx: Dict, candidates: List[Dict],
    gap_topics: List[str], next_topics: List[str], *, runnable=None,
) -> Dict:
    """
    Re-ranks the candidates with the full profile in context.
    The prompt includes: skill level, languages, topics, gaps, error patterns,
    time spent, accuracy rate — so explanations are genuinely personalised.
    """
    cids        = [c["content_id"] for c in candidates]
    contents    = db.query(Content).filter(Content.id.in_(cids)).all()
    content_map = {c.id: c for c in contents}

    summaries = []
    for c in candidates:
        cobj = content_map.get(c["content_id"])
        if not cobj:
            continue
        summaries.append({
            "id":            c["content_id"],
            "title":         cobj.title,
            "type":          cobj.content_type.value,
            "difficulty":    cobj.difficulty.value,
            "language":      cobj.language or "general",
            "topics":        cobj.topics,
            "skills_gained": cobj.skills_gained,
            "duration_mins": cobj.duration_mins,
            "has_url":       bool(cobj.url),
            "blended_score": c["blended_score"],
            "cf_score":      c["cf_score"],
            "cbf_score":     c["cbf_score"],
            "is_expansion":  c.get("is_expansion", False),
        })

    # Build time-spent summary for the prompt
    time_summary = ", ".join(
        f"{t}: {int(m)}min" for t, m in
        sorted(user_ctx["time_per_topic"].items(), key=lambda x: -x[1])[:5]
    ) or "no history yet"

    system_prompt = f"""You are a personalized video recommendation assistant inside aiTA.

User Profile:
- Skill Level: {user_ctx['skill_level']}
- Preferred Language: {', '.join(user_ctx['preferred_languages']) or 'not specified'}
- Interested Topics: {', '.join(user_ctx['interested_topics']) or 'not set'}
- Learning Goals: {', '.join(user_ctx.get('learning_goals', [])) or 'not specified'}
- Weak Areas: {', '.join(user_ctx['weak_areas']) or 'none'}
- Recommended Next Topics: {', '.join(next_topics) or 'continue current topics'}

Additional context:
- Knowledge gaps (low accuracy): {', '.join(gap_topics) or 'none detected'}
- Error patterns: {', '.join(user_ctx['error_patterns'][:3]) or 'none'}
- Accuracy rate: {user_ctx['accuracy_rate']:.0%}
- Time spent per topic: {time_summary}

Task:
Recommend {TOP_N} videos (5–8) tailored to this user from the candidates below.

Guidelines:
- Match difficulty to skill level ({user_ctx['skill_level']})
- Prioritize interested_topics and learning_goals
- Focus on weak_areas and recommended_next for improvement
- Prefer videos in the user's preferred language
- Prefer items with has_url: true (real video links)
- Diversify content types when possible
- Expansion items (is_expansion: true) rank lower unless gaps are exhausted"""

    user_prompt = f"Candidates:\n{json.dumps(summaries, indent=2)}"

    try:
        payload = [("system", system_prompt), ("human", user_prompt)]
        if runnable is None:
            result = llm_gateway.invoke("ranking", payload, schema=RankedRecommendations,
                                        user_id=user_ctx.get("user_id"))
            parsed, tokens, model = result.value, result.tokens, result.model
        else:
            parsed, usage = invoke_with_retry(runnable, payload)
            tokens, model = usage.tokens, usage.model
    except LLMUnavailable as exc:
        logger.warning("Re-ranking unavailable, falling back to score order: %s",
                       exc.detail)
        return _score_ordered(candidates, exc.detail)

    if parsed is None:
        # Structured output that failed to parse leaves nothing to rank by, which is
        # the same situation for the student as no call at all.
        logger.warning("Re-ranking returned no parseable structure, "
                       "falling back to score order")
        return _score_ordered(candidates, "the ranking could not be read")

    return {
        "ranked_ids":   [item.id for item in parsed.ranked],
        "explanations": {
            str(item.id): f"{item.description} {item.why_relevant}".strip()
            for item in parsed.ranked
        },
        "descriptions": {str(item.id): item.description for item in parsed.ranked},
        "difficulties": {str(item.id): item.difficulty for item in parsed.ranked},
        "summary":      parsed.summary,
        "tokens_used":  tokens,
        "model_used":   model,
    }
