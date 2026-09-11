from app.agents.code_eval.state import EvalState
from app.core.exceptions import SubmissionNotFound
from app.core.languages import EXECUTABLE_LANGUAGES
from app.models.code_eval import CodeSubmission
from app.models.problem import ProblemSource
from app.models.user import User
from app.services.problems.repository import get_or_create_problem


def route_mode(state: EvalState) -> EvalState:
    submission = (
        state.db.query(CodeSubmission)
        .filter(
            CodeSubmission.id == state.submission_id,
            CodeSubmission.user_id == state.user_id,
        )
        .first()
    )
    if submission is None:
        raise SubmissionNotFound(f"submission {state.submission_id} not found")

    state.language = submission.language
    state.code = submission.code

    user = state.db.query(User).filter(User.id == state.user_id).first()
    if user is not None and user.skill_level is not None:
        state.skill_level = getattr(user.skill_level, "value", str(user.skill_level))

    if submission.language not in EXECUTABLE_LANGUAGES:
        state.mode = "review"
        state.unverified_reason = "language_not_executable"
        state.log(f"Review mode: {submission.language.value} is not executable.")
        return state

    if not (submission.problem_context or "").strip():
        state.mode = "review"
        state.unverified_reason = "no_problem_statement"
        state.log("Review mode: no problem statement supplied.")
        return state

    problem, created = get_or_create_problem(
        state.db,
        submission.problem_context,
        source=ProblemSource.STUDENT,
        created_by_user_id=state.user_id,
    )
    if submission.problem_id != problem.id:
        submission.problem_id = problem.id
        state.db.commit()

    state.problem_id = problem.id
    state.problem_statement = problem.statement
    state.mode = "verified"
    state.log(
        f"Verified mode: problem {problem.id} "
        f"({'new' if created else 'existing'}), {len(problem.test_cases)} cached cases."
    )
    return state
