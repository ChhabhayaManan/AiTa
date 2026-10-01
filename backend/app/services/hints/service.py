"""One hint ladder shared by Code Eval (L1, template) and Feedback (L2-L4, LLM).

Ladder position is measured in evaluation ids, not wall-clock time: a hint belongs to
the evaluation it was about, and a fully passing evaluation resets the ladder."""

from dataclasses import dataclass

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.exceptions import AitaError, LLMUnavailable
from app.core.llm import get_chat_model, invoke_with_retry
from app.models.code_eval import CodeEvaluation, CodeSubmission
from app.models.learning import HintEvent
from app.models.problem import (
    ExecRole,
    ExecutionResult,
    Problem,
    ReferenceStatus,
    TestCase,
)
from app.services.hints import guardrail
from app.services.hints.prompts import HINT_PROMPT, LEVEL_INSTRUCTIONS, TEMPLATES
from app.services.profiling.service import top_misconceptions

MAX_LEVEL = 4
_CRASH_STATUSES = ("runtime_error", "timeout", "memory_exceeded")


class NoHintAvailable(AitaError):
    status_code = 409


@dataclass
class FailingCase:
    stdin: str
    expected: str
    actual: str
    rationale: str | None = None
    status: str = "wrong_answer"


@dataclass
class Hint:
    level: int
    text: str
    source: str
    was_blocked: bool
    evaluation_id: int
    problem_id: int


def _evaluations(db: Session, user_id: int, problem_id: int):
    return (
        db.query(CodeEvaluation)
        .join(CodeSubmission, CodeSubmission.id == CodeEvaluation.submission_id)
        .filter(CodeEvaluation.user_id == user_id, CodeSubmission.problem_id == problem_id)
    )


def _passed(evaluation: CodeEvaluation) -> bool:
    return bool(evaluation.tests_total) and evaluation.tests_passed == evaluation.tests_total


def last_pass_id(db: Session, user_id: int, problem_id: int, before: int | None = None) -> int:
    query = _evaluations(db, user_id, problem_id).filter(
        CodeEvaluation.tests_total > 0,
        CodeEvaluation.tests_passed == CodeEvaluation.tests_total,
    )
    if before is not None:
        query = query.filter(CodeEvaluation.id < before)
    return query.with_entities(func.max(CodeEvaluation.id)).scalar() or 0


def highest_level(db: Session, user_id: int, problem_id: int, before: int | None = None) -> int:
    """Highest hint level seen on this problem since the last full pass. With `before`,
    only hints about evaluations earlier than that one count."""
    query = db.query(func.max(HintEvent.level)).filter(
        HintEvent.user_id == user_id,
        HintEvent.problem_id == problem_id,
        HintEvent.evaluation_id > last_pass_id(db, user_id, problem_id, before),
    )
    if before is not None:
        query = query.filter(HintEvent.evaluation_id < before)
    return query.scalar() or 0


def next_level(db: Session, user_id: int, problem_id: int) -> int:
    return min(MAX_LEVEL, highest_level(db, user_id, problem_id) + 1)


def l1_text(case: FailingCase) -> str:
    if case.status in _CRASH_STATUSES:
        return (
            f"Your program stopped early ({case.status.replace('_', ' ')}) on this input:\n"
            f"{case.stdin.rstrip()}\n"
            "What does your code do with it just before it stops?"
        )
    checks = f" This case checks: {case.rationale}." if case.rationale else ""
    return (
        f"Your code fails on this input:\n{case.stdin.rstrip()}\n"
        f"Expected `{case.expected}`, but it printed `{case.actual}`.{checks} "
        "Trace your code by hand on it: what value does each variable hold at the end?"
    )


def log_hint(db: Session, *, user_id: int, problem_id: int, evaluation_id: int,
             level: int, was_blocked: bool = False) -> HintEvent:
    event = HintEvent(user_id=user_id, problem_id=problem_id, evaluation_id=evaluation_id,
                      level=level, was_blocked=was_blocked)
    db.add(event)
    db.commit()
    return event


def leak_rate(db: Session) -> tuple[int, int]:
    """(blocked, total) over LLM-written hints. L1 is a template and cannot leak."""
    rows = db.query(HintEvent.was_blocked).filter(HintEvent.level >= 2).all()
    return sum(1 for (blocked,) in rows if blocked), len(rows)


def reference_sources(problem: Problem | None) -> list[str]:
    """Validated references, for the guardrail's prose check only. Never returned."""
    if problem is None:
        return []
    return [r.source for r in problem.references if r.status is ReferenceStatus.VALIDATED]


def failing_case(db: Session, evaluation: CodeEvaluation) -> FailingCase | None:
    rows = (
        db.query(ExecutionResult)
        .filter(ExecutionResult.evaluation_id == evaluation.id,
                ExecutionResult.role == ExecRole.STUDENT)
        .order_by(ExecutionResult.id)
        .all()
    )
    for row in rows:
        if row.status == "ok":
            continue
        case = db.get(TestCase, row.test_case_id) if row.test_case_id else None
        return FailingCase(
            stdin=case.stdin if case else "",
            expected=case.expected_stdout if case else "",
            actual=row.stdout or "",
            rationale=case.rationale if case else None,
            status=row.status,
        )
    return None


def _llm_hint(level: int, context: dict, runnable) -> str:
    prompt = HINT_PROMPT.format(
        level_instruction=LEVEL_INSTRUCTIONS[level],
        max_lines=guardrail.max_code_lines(level),
        **context,
    )
    message, _ = invoke_with_retry(runnable, prompt)
    return (getattr(message, "content", message) or "").strip()


def request_hint(db: Session, user_id: int, problem_id: int, *, runnable=None,
                 provider=None) -> Hint:
    evaluation = _evaluations(db, user_id, problem_id).order_by(CodeEvaluation.id.desc()).first()
    if evaluation is None:
        raise NoHintAvailable("Submit an attempt at this problem first.")
    if _passed(evaluation):
        raise NoHintAvailable("Your last attempt passed every test. No hint needed.")

    problem = db.get(Problem, problem_id)
    submission = db.get(CodeSubmission, evaluation.submission_id)
    case = failing_case(db, evaluation) or FailingCase(stdin="", expected="", actual="")
    level = next_level(db, user_id, problem_id)

    if level == 1:
        hint = Hint(1, l1_text(case), "template", False, evaluation.id, problem_id)
    else:
        hint = _ladder_hint(db, level, problem, submission, case, user_id, evaluation.id,
                            runnable, provider)

    log_hint(db, user_id=user_id, problem_id=problem_id, evaluation_id=evaluation.id,
             level=hint.level, was_blocked=hint.was_blocked)
    return hint


def _ladder_hint(db, level, problem, submission, case, user_id, evaluation_id,
                 runnable, provider) -> Hint:
    seen = [tag for tag, _ in top_misconceptions(db, user_id)[:3]]
    context = {
        "statement": problem.statement if problem else "",
        "language": submission.language.value,
        "code": submission.code,
        "stdin": repr(case.stdin),
        "expected": repr(case.expected),
        "actual": repr(case.actual),
        "misconceptions": ", ".join(seen) or "none recorded",
    }
    tests = list(problem.test_cases) if problem else []
    references = reference_sources(problem)

    blocked = False
    try:
        runnable = runnable or get_chat_model(temperature=0.4)
        for _ in range(2):
            text = _llm_hint(level, context, runnable)
            verdict = guardrail.check(text, level, submission.language, tests, provider,
                                      references=references, student_code=submission.code)
            if text and not verdict.blocked:
                return Hint(level, text, "llm", blocked, evaluation_id, problem.id)
            blocked = blocked or verdict.blocked
    except LLMUnavailable:
        pass
    return Hint(level, TEMPLATES[level], "template", blocked, evaluation_id, problem.id)
