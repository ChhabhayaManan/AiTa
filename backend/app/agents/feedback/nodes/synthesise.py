import json
import logging

from app.agents.feedback.prompts import (
    CP_BLOCK,
    EVAL_BLOCK,
    PATTERN_BLOCK,
    PATTERN_ONLY_HEADLINE,
    PATTERN_ONLY_MOTIVATIONAL,
    SYSTEM_PROMPT,
    TONE_INSTRUCTIONS,
)
from app.agents.feedback.schemas import FeedbackNarrative
from app.agents.feedback.state import FeedbackState
from app.core.exceptions import LLMUnavailable
from app.core.llm import get_chat_model, invoke_with_retry, structured

logger = logging.getLogger(__name__)

# `steps` is persisted and shown to the student, so the failure step says only what a
# student can act on. The provider's own error text — which can carry the host, the
# model id and an API error body — goes to the log instead.
PATTERN_ONLY_STEP = ("Detailed feedback could not be generated. "
                     "Reporting the pattern analysis on its own.")


def _score(value) -> str:
    return "n/a" if value is None else f"{value:.0f}"


def _fmt_correctness(eval_ctx: dict) -> str:
    score = eval_ctx.get("correctness")
    if score is None:
        return f"unverified ({eval_ctx.get('verification', 'unknown')})"
    return f"{score:.0f} ({eval_ctx.get('tests_passed', 0)}/{eval_ctx.get('tests_total', 0)} tests)"


def _system(state: FeedbackState) -> str:
    ctx = state.user_ctx
    return SYSTEM_PROMPT.format(
        username=ctx["username"],
        skill=ctx["skill"],
        languages=", ".join(ctx["languages"]) or "general",
        weak_areas=", ".join(ctx["weak_areas"]) or "none yet",
        tone_instruction=TONE_INSTRUCTIONS[state.tone],
    )


def _context(state: FeedbackState) -> str:
    patterns = state.patterns
    parts = []
    if state.eval_ctx:
        e = state.eval_ctx
        parts.append(EVAL_BLOCK.format(
            overall=_score(e["overall"]),
            correctness=_fmt_correctness(e),
            complexity=_score(e["complexity"]),
            efficiency=_score(e["efficiency"]),
            issues=json.dumps(patterns["errors"]),
            learning_points=json.dumps(e["learning_points"][:5]),
            anti_patterns=json.dumps(e["anti_patterns"][:4]),
            summary=e["summary"],
        ))
    if state.cp_ctx:
        c = state.cp_ctx
        parts.append(CP_BLOCK.format(
            topic=c["topic"],
            mode=c["mode"],
            concepts=json.dumps(c["concepts"][:8]),
            mastery=json.dumps(c["mastery"][:5]),
            weak=json.dumps(c["weak"][:5]),
            confusion=c["confusion"],
        ))
    parts.append(PATTERN_BLOCK.format(
        errors=json.dumps(patterns["errors"]),
        weak_concepts=json.dumps(patterns["weak_concepts"]),
        strengths=json.dumps(patterns["strengths"]),
    ))
    return "\n\n".join(parts)


def _from_patterns(patterns: dict) -> FeedbackNarrative:
    """The degraded narrative. It says outright that it is not the real analysis —
    the previous implementation returned this shape silently and the UI showed it
    as if a model had written it."""
    return FeedbackNarrative(
        headline=PATTERN_ONLY_HEADLINE,
        summary=(
            "This comes from automatic pattern analysis only, because detailed "
            "feedback could not be generated. Patterns found: "
            f"{', '.join(patterns['errors'][:2]) or 'none'}."
        ),
        strengths=patterns["strengths"],
        errors=patterns["errors"],
        misconceptions=[],
        action_items=[f"Review: {c}" for c in patterns["weak_concepts"][:3]],
        concept_map={c: 0.3 for c in patterns["weak_concepts"]},
        next_topics=patterns["weak_concepts"][:3],
        motivational=PATTERN_ONLY_MOTIVATIONAL,
    )


def synthesise(state: FeedbackState) -> FeedbackState:
    state.log("Synthesising personalised feedback.")
    try:
        runnable = (state.synthesise_runnable
                    or structured(get_chat_model(temperature=0.4), FeedbackNarrative))
        narrative, usage = invoke_with_retry(
            runnable, [("system", _system(state)), ("human", _context(state))]
        )
    except LLMUnavailable as exc:
        logger.warning("Feedback synthesis unavailable for user %s: %s",
                       state.user_id, exc.detail)
        state.pattern_only = True
        state.narrative = _from_patterns(state.patterns)
        state.log(PATTERN_ONLY_STEP)
        return state

    if narrative is None:
        # Structured output that failed to parse is the same situation as no call at
        # all, and must be labelled the same way rather than persisted as empty prose.
        logger.warning("Feedback synthesis returned no parsed narrative for user %s",
                       state.user_id)
        state.pattern_only = True
        state.narrative = _from_patterns(state.patterns)
        state.log(PATTERN_ONLY_STEP)
        return state

    state.narrative = narrative
    state.tokens_used = usage.tokens
    state.log(f"Feedback synthesised ({usage.tokens} tokens).")
    return state
