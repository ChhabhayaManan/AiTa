import time

from app.agents.feedback.state import FeedbackState
from app.core.text import ellipsize
from app.models.feedback import FeedbackReport
from app.services.feedback.profile import update_profile

HEADLINE_LIMIT = 300


def persist(state: FeedbackState) -> FeedbackState:
    narrative = state.narrative.model_dump()

    state.log("Writing signals back to the learning profile.")
    state.profile_updates = update_profile(
        state.db, state.user_id, state.patterns, narrative
    )
    state.log(f"Updated: {list(state.profile_updates.keys())}")

    duration = int(time.time() * 1000) - state.started_ms
    state.log(f"Done in {duration}ms")

    report = FeedbackReport(
        user_id=state.user_id,
        evaluation_id=state.evaluation_id,
        cp_session_id=state.cp_session_id,
        feedback_type=state.feedback_type,
        tone=state.tone,
        # The only bounded column in the row, and update_profile has already
        # committed by now — an over-long headline must not discard the report.
        headline=ellipsize(narrative["headline"], HEADLINE_LIMIT),
        summary=narrative["summary"],
        strengths=narrative["strengths"],
        errors=narrative["errors"],
        misconceptions=narrative["misconceptions"],
        action_items=narrative["action_items"],
        concept_map=narrative["concept_map"],
        next_topics=narrative["next_topics"],
        motivational=narrative["motivational"],
        profile_updates=state.profile_updates,
        agent_steps=state.steps,
        tokens_used=state.tokens_used,
        latency_ms=duration,
        pattern_only=state.pattern_only,
    )
    state.db.add(report)
    state.db.commit()
    state.db.refresh(report)
    state.report = report
    return state
