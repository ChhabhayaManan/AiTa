"""Graders for the non-coding items. Neither calls an LLM; both hand their evidence to
the Profiling Agent. The answer key and the fixed program only leave after grading."""

import logging
from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from app.agents.code_eval.multi_test import verdict_for
from app.agents.profiling.graph import ingest
from app.core.exceptions import AitaError
from app.models.code_eval import Language
from app.models.learning import DebugAttempt, DebugChallenge, McqAttempt, McqQuestion
from app.models.problem import Problem
from app.services.execution.judge import judge
from app.services.gamification.service import awards_for_event
from app.services.profiling.mastery import debug_score
from app.services.profiling.service import EventInput

logger = logging.getLogger(__name__)


class ItemNotFound(AitaError):
    status_code = 404


class InvalidAnswer(AitaError):
    status_code = 422


@dataclass
class McqResult:
    correct: bool
    chosen_index: int
    answer_index: int
    misconception: str | None
    explanation: str | None
    mastery_after: float | None
    awards: list[dict] = field(default_factory=list)


@dataclass
class DebugResult:
    fixed: bool
    verdict: str
    tests_passed: int
    tests_total: int
    failing_input: str | None
    failing_expected: str | None
    failing_actual: str | None
    mastery_after: float | None
    awards: list[dict] = field(default_factory=list)


def grade_mcq(db: Session, user_id: int, question_id: int, chosen_index: int) -> McqResult:
    question = db.get(McqQuestion, question_id)
    if question is None or not question.reviewed:
        raise ItemNotFound(f"question {question_id} not found")
    if not 0 <= chosen_index < len(question.options):
        raise InvalidAnswer("chosen_index is out of range")

    correct = chosen_index == question.answer_index
    misconception = None if correct else question.options[chosen_index].get("misconception")
    attempt = McqAttempt(user_id=user_id, question_id=question.id,
                         chosen_index=chosen_index, correct=correct)
    db.add(attempt)
    db.flush()

    event = ingest(db, EventInput(
        user_id=user_id,
        kind="diagnostic" if question.is_diagnostic else "mcq",
        score=1.0 if correct else 0.0,
        raw_topic=question.topic,
        item_id=question.id,
        misconceptions=[misconception] if misconception else [],
        source_ref=f"mcq_attempt:{attempt.id}",
    ))
    explanations = question.explanations or []
    return McqResult(correct, chosen_index, question.answer_index, misconception,
                     explanations[0] if explanations else None, event.mastery_after,
                     _awards(db, event.id))


def grade_debug(db: Session, user_id: int, challenge_id: int, code: str,
                provider=None) -> DebugResult:
    challenge = db.get(DebugChallenge, challenge_id)
    if challenge is None or not challenge.reviewed:
        raise ItemNotFound(f"debug challenge {challenge_id} not found")
    problem = db.get(Problem, challenge.problem_id)

    result = judge(Language(challenge.language), code, problem.test_cases, provider)
    split = result.split
    fixed = result.all_passed
    failing = split.first_failing

    attempt = DebugAttempt(user_id=user_id, challenge_id=challenge.id, submitted_code=code,
                           tests_passed=split.passed, tests_total=split.total, fixed=fixed)
    db.add(attempt)
    db.flush()

    event = ingest(db, EventInput(
        user_id=user_id,
        kind="debug",
        score=debug_score(fixed, split.passed, split.total),
        raw_topic=challenge.topic,
        item_id=challenge.id,
        misconceptions=[] if fixed else [challenge.bug_type],
        source_ref=f"debug_attempt:{attempt.id}",
    ))

    return DebugResult(
        fixed=fixed,
        verdict=verdict_for(result.status, split),
        tests_passed=split.passed,
        tests_total=split.total,
        failing_input=failing.stdin if failing else None,
        failing_expected=failing.expected_stdout if failing else None,
        failing_actual=failing.actual_stdout if failing else None,
        mastery_after=event.mastery_after,
        awards=_awards(db, event.id),
    )


def _awards(db: Session, event_id: int) -> list[dict]:
    """The answer is already graded and committed; a toast must never turn it into a 500."""
    try:
        return [a.model_dump() for a in awards_for_event(db, event_id)]
    except Exception:
        logger.exception("award lookup failed for event %s", event_id)
        return []
