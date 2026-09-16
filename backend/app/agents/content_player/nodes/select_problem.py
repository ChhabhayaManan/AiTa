import logging

from app.agents.content_player.state import ChatState
from app.core.exceptions import LLMUnavailable
from app.services.problems import generation
from app.services.problems.listing import to_summary
from app.services.problems.picker import pick_problem, resolve_difficulty

logger = logging.getLogger(__name__)


def _should_serve(state: ChatState) -> bool:
    """The two moments the agent has always asked for a problem: the opening of a
    walkthrough, and the turn after the student solved one."""
    if state.question_solved:
        return True
    return (state.mode == "walkthrough"
            and len(state.history) <= 1
            and "problem" not in state.message.lower())


def select_problem(state: ChatState) -> ChatState:
    if not _should_serve(state):
        return state

    # Resolved the same way the /generate-problem endpoint resolves it.
    difficulty = resolve_difficulty(state.new_difficulty)

    picked = pick_problem(
        state.db,
        topic=state.effective_topic,
        difficulty=difficulty,
        exclude_ids=state.solved_questions,
    )
    if picked is not None:
        state.problem_id = picked.id
        state.problem_statement = to_summary(picked).statement
        state.problem_origin = "bank"
        return state

    try:
        result = generation.generate_problem(
            state.db, topic=state.effective_topic, difficulty=difficulty
        )
    except LLMUnavailable as exc:
        logger.warning("Problem generation unavailable for session %s: %s",
                       state.session_id, exc.detail)
        state.problem_origin = "improvised"
        return state

    if result.ungradeable_reason:
        # The row survives for a later attempt, but a problem nothing can mark is not
        # something to set a student.
        logger.warning("Generated problem %s is not gradeable (%s)",
                       result.problem.id, result.ungradeable_reason)
        state.problem_origin = "improvised"
        return state

    state.problem_id = result.problem.id
    state.problem_statement = to_summary(result.problem).statement
    state.problem_origin = "generated"
    return state
