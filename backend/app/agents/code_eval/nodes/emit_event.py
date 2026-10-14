import logging

from app.agents.code_eval.state import EvalState
from app.agents.profiling.graph import ingest
from app.models.problem import Problem
from app.services.gamification.service import awards_for_event
from app.services.hints.service import highest_level
from app.services.profiling.mastery import code_score
from app.services.profiling.service import EventInput

logger = logging.getLogger(__name__)


def emit_event(state: EvalState) -> EvalState:
    """Hand the graded attempt to the Profiling Agent. Only verified runs are evidence:
    review mode has no measured pass rate to learn from. The attempt is discounted by
    the highest Practice hint seen on this problem before it was submitted; chat is not
    practice and never moves mastery."""
    report = state.report
    if (report is None or report.evaluation_id is None
            or report.verification_status != "verified" or not report.tests_total
            or state.problem_id is None):
        return state

    problem = state.db.get(Problem, state.problem_id)
    try:
        hint_level = highest_level(state.db, state.user_id, state.problem_id,
                                   before=report.evaluation_id, sources=("practice",))
        event = ingest(state.db, EventInput(
            user_id=state.user_id,
            kind="code",
            score=code_score(report.tests_passed, report.tests_total, hint_level),
            raw_topic=problem.topic if problem else None,
            item_id=state.problem_id,
            hint_level=hint_level,
            misconceptions=report.misconceptions,
            source_ref=f"evaluation:{report.evaluation_id}",
        ))
        report.awards = awards_for_event(state.db, event.id)
    except Exception:
        # The evaluation is already committed and returned; a profiling failure must
        # not turn a graded submission into a 500.
        state.db.rollback()
        logger.exception("profiling failed for evaluation %s", report.evaluation_id)
    return state
