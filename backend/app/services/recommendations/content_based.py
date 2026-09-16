from typing import Dict, List

from sqlalchemy.orm import Session

from app.models.recommendation import Content
from app.services.recommendations.weights import TOPIC_ADJACENCY


def _content_based_filtering(db: Session, user_ctx: Dict, gap_topics: List[str]) -> Dict[int, float]:
    """
    Profile-driven CBF with gap-aware scoring.

    Scoring priority:
      1. Gap topics (low accuracy / error patterns) — highest boost
      2. Interested topics from profile
      3. Weak areas (agent-detected)
      4. Language match
      5. Difficulty alignment (skill_level + difficulty_pref)
      6. Learning goals / interests
      7. Preferred content types
      8. Quality signal (avg_rating)
    """
    excluded = user_ctx["excluded_ids"] | user_ctx["seen_content_ids"]
    contents = db.query(Content).filter(
        Content.is_active.is_(True),
        ~Content.id.in_(excluded or {0}),
    ).all()

    skill_map     = {"beginner": 0, "intermediate": 1, "advanced": 2}
    user_skill    = skill_map.get(user_ctx["skill_level"], 0)
    diff_pref_map = {"easy": 0, "medium": 1, "hard": 2}
    target_diff   = diff_pref_map.get(user_ctx["difficulty_pref"], user_skill)

    gap_set       = {t.lower() for t in gap_topics}
    interested    = {t.lower().replace("_", " ") for t in user_ctx["interested_topics"]}
    weak_areas    = {t.lower() for t in user_ctx["weak_areas"]}
    pref_langs    = {lang.lower() for lang in user_ctx["preferred_languages"]}
    interests     = {t.lower() for t in user_ctx["interests"]}
    goals         = {g.lower() for g in user_ctx["learning_goals"]}
    pref_types    = {t.lower() for t in user_ctx["preferred_content_types"]}
    topic_scores  = {k.lower(): v for k, v in user_ctx["topic_scores"].items()}
    error_topics  = {e.lower() for e in user_ctx["error_patterns"]}

    cbf_scores: Dict[int, float] = {}

    for c in contents:
        score    = 0.0
        c_topics = {t.lower().replace("_", " ") for t in (c.topics or [])}
        c_skills = {s.lower() for s in (c.skills_gained or [])}
        c_lang   = (c.language or "").lower()
        c_diff   = skill_map.get(c.difficulty.value, 0)

        # 1. Gap topics — highest priority (student needs this most)
        gap_overlap = c_topics & gap_set
        if gap_overlap:
            score += min(len(gap_overlap) * 0.30, 0.60)

        # 2. Interested topics from profile
        topic_overlap = c_topics & interested
        if topic_overlap:
            score += min(len(topic_overlap) * 0.20, 0.40)
            # Extra boost for topics with low mastery score
            for t in topic_overlap:
                ts = topic_scores.get(t, 0.5)
                if ts < 0.5:
                    score += 0.08

        # 3. Error pattern topics — student keeps making mistakes here
        error_overlap = c_topics & error_topics
        score += min(len(error_overlap) * 0.12, 0.24)

        # 4. Weak areas (agent-detected)
        weak_overlap = c_topics & weak_areas
        score += min(len(weak_overlap) * 0.10, 0.20)

        # 5. Language match
        if c_lang and c_lang in pref_langs:
            score += 0.15
        elif c_lang in ("general", ""):
            score += 0.03

        # 6. Difficulty alignment
        diff_gap = abs(c_diff - target_diff)
        if diff_gap == 0:
            score += 0.20
        elif diff_gap == 1:
            score += 0.08

        # 7. Interests + learning goals
        score += min(len(c_topics & interests) * 0.05, 0.10)
        score += min(len(c_skills & goals) * 0.04, 0.08)

        # 8. Preferred content type
        if pref_types and c.content_type.value in pref_types:
            score += 0.06

        # 9. Quality signal
        if c.avg_rating >= 4.5:
            score += 0.05
        elif c.avg_rating >= 4.0:
            score += 0.02

        cbf_scores[c.id] = min(score, 1.0)

    return cbf_scores


def _expand_related_topics(db: Session, user_ctx: Dict, next_topics: List[str]) -> Dict[int, float]:
    """Finds content on adjacent/prerequisite topics when fresh content is scarce."""
    excluded  = user_ctx["excluded_ids"] | user_ctx["seen_content_ids"]
    interested = {t.lower().replace("_", " ") for t in user_ctx["interested_topics"]}
    pref_langs = {lang.lower() for lang in user_ctx["preferred_languages"]}
    skill_map  = {"beginner": 0, "intermediate": 1, "advanced": 2}
    user_skill = skill_map.get(user_ctx["skill_level"], 0)
    diff_pref_map = {"easy": 0, "medium": 1, "hard": 2}
    target_diff = diff_pref_map.get(user_ctx["difficulty_pref"], user_skill)

    # Combine next_topics with adjacency suggestions
    related = set(next_topics)
    for topic in interested:
        for adj in TOPIC_ADJACENCY.get(topic, []):
            if adj not in interested:
                related.add(adj)

    if not related:
        return {}

    all_unseen = db.query(Content).filter(
        Content.is_active.is_(True),
        ~Content.id.in_(excluded or {0}),
    ).all()

    expansion: Dict[int, float] = {}
    for c in all_unseen:
        c_topics = {t.lower().replace("_", " ") for t in (c.topics or [])}
        overlap  = c_topics & related
        if not overlap:
            continue
        score = min(len(overlap) * 0.18, 0.36)
        c_diff = skill_map.get(c.difficulty.value, 0)
        if abs(c_diff - target_diff) == 0:
            score += 0.12
        elif abs(c_diff - target_diff) == 1:
            score += 0.04
        if (c.language or "").lower() in pref_langs:
            score += 0.08
        expansion[c.id] = min(score * 0.75, 0.55)  # slightly lower than direct match

    return expansion
