"""Practice entry points feed the session lifecycle; other surfaces never join it."""

from datetime import datetime, timezone

import pytest

from app.agents.code_eval.graph import evaluate_submission
from app.api.assessment import get_next
from app.core.exceptions import LLMUnavailable
from app.models.learning import LearningEvent
from app.models.onboarding import OnboardingRecord
from app.models.practice_session import PracticeSession
from app.models.problem import Problem, ProblemSource, TestCase, TestCaseKind, TestCaseOrigin
from app.models.user import User
from app.services.assessment import policy
from app.services.assessment.grading import grade_mcq
from app.services.onboarding.recheck import switch_language
from app.services.practice_session import lifecycle
from tests.agents.test_emit_event import explain_with, submit
from tests.agents.test_graph import merged
from tests.conftest import FakeExecutionProvider
from tests.services.assessment.test_policy import add_mcq


@pytest.fixture
def user(session):
    u = User(email="w@example.com", username="wired", hashed_password="x",
             preferred_language="c")
    session.add(u)
    session.commit()
    return u


def graded_problem(session, n):
    p = Problem(source=ProblemSource.DSA, statement=f"max {n}", statement_hash=f"{n:064d}",
                topic="arrays")
    p.test_cases = [
        TestCase(kind=TestCaseKind.SAMPLE, stdin="1\n5\n", expected_stdout="5",
                 stdin_hash="a", origin=TestCaseOrigin.PROBLEM_SAMPLE, ordinal=0),
        TestCase(kind=TestCaseKind.EDGE, stdin="1\n-7\n", expected_stdout="-7",
                 stdin_hash="b", origin=TestCaseOrigin.CROSS_CHECKED, ordinal=1),
    ]
    session.add(p)
    session.commit()
    return p


def test_mcq_answer_attaches_to_session(session, user, monkeypatch):
    def refuse(*a, **k):
        raise LLMUnavailable("generation is stubbed in tests")
    monkeypatch.setattr(policy, "generate_problem", refuse)
    question = add_mcq(session, "basics_io")

    served = get_next(current_user=user, db=session)
    grade_mcq(session, user.id, served["item"]["id"], 0)

    practice = session.query(PracticeSession).one()
    assert served["item"]["id"] == question.id
    assert session.query(LearningEvent).one().session_id == practice.id
    assert practice.graded_count == 1


def test_workspace_submit_not_in_session(session, user):
    served, workspace = graded_problem(session, 7), graded_problem(session, 9)
    lifecycle.record_served(session, user.id, "coding", served.id, "python",
                            datetime.now(timezone.utc))
    session.commit()

    evaluate_submission(session, submit(session, user, workspace.id).id, user.id,
                        provider=FakeExecutionProvider(merged("5\n-7\n")),
                        explain_runnable=explain_with([]))

    assert session.query(LearningEvent).one().session_id is None
    assert session.query(PracticeSession).one().graded_count == 0


def test_switch_language_closes_session(session, user):
    now = datetime.now(timezone.utc)
    session.add(OnboardingRecord(user_id=user.id, finished_at=now, language="c"))
    practice = lifecycle.record_served(session, user.id, "mcq", 1, "c", now)
    event = LearningEvent(user_id=user.id, kind="mcq", item_id=1, score=1.0, weight=0.5,
                          language="c")
    session.add(event)
    session.flush()
    lifecycle.attach_event(session, event, "mcq", now)
    session.commit()

    switch_language(session, user, "cpp")

    assert session.get(PracticeSession, practice.id).end_reason == "language_switch"
