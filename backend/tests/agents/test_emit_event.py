"""Code Eval → Profiling Agent wiring. Stubbed executor and explanation."""

import pytest

from app.agents.code_eval.graph import evaluate_submission
from app.agents.code_eval.schemas import Explanation
from app.models.code_eval import CodeSubmission, Language
from app.models.learning import LearningEvent, TopicMastery
from app.models.problem import (
    Problem,
    ProblemSource,
    TestCase,
    TestCaseKind,
    TestCaseOrigin,
)
from app.models.user import User
from tests.agents.test_graph import FakeExplainRunnable, merged
from tests.conftest import FakeExecutionProvider


@pytest.fixture
def user(session):
    u = User(email="e@example.com", username="emitter", hashed_password="x")
    session.add(u)
    session.commit()
    return u


@pytest.fixture
def problem(session):
    p = Problem(source=ProblemSource.DSA, statement="max", statement_hash="e" * 64,
                topic="dynamic_programming")
    p.test_cases = [
        TestCase(kind=TestCaseKind.SAMPLE, stdin="1\n5\n", expected_stdout="5",
                 stdin_hash="a", origin=TestCaseOrigin.PROBLEM_SAMPLE, ordinal=0),
        TestCase(kind=TestCaseKind.EDGE, stdin="1\n-7\n", expected_stdout="-7",
                 stdin_hash="b", origin=TestCaseOrigin.CROSS_CHECKED, ordinal=1),
    ]
    session.add(p)
    session.commit()
    return p


def submit(session, user, problem_id=None, language=Language.PYTHON):
    s = CodeSubmission(user_id=user.id, language=language, code="print(0)",
                       problem_id=problem_id, title="t")
    session.add(s)
    session.commit()
    return s


def explain_with(tags):
    return FakeExplainRunnable(Explanation(
        summary="s", detailed_feedback="## f", misconceptions=tags,
    ))


def test_verified_submission_emits_one_event_and_moves_mastery(session, user, problem):
    submission = submit(session, user, problem.id)
    report = evaluate_submission(
        session, submission.id, user.id,
        provider=FakeExecutionProvider(merged("5\n0\n")),
        explain_runnable=explain_with(["wrong_initial_value", "not_a_tag"]),
    )

    assert (report.tests_passed, report.tests_total) == (1, 2)
    assert report.misconceptions == ["wrong_initial_value"]

    event = session.query(LearningEvent).one()
    assert event.kind == "code"
    assert event.topic == "dynamic_programming"
    assert event.score == pytest.approx(0.5)
    assert event.item_id == problem.id
    assert event.misconceptions == ["wrong_initial_value"]
    assert event.source_ref == f"evaluation:{report.evaluation_id}"

    row = session.get(TopicMastery, (user.id, "dynamic_programming"))
    assert row.mastery == pytest.approx(0.3 + 0.3 * (0.5 - 0.3))


def test_passing_submission_carries_no_misconceptions(session, user, problem):
    submission = submit(session, user, problem.id)
    report = evaluate_submission(
        session, submission.id, user.id,
        provider=FakeExecutionProvider(merged("5\n-7\n")),
        explain_runnable=explain_with(["off_by_one"]),
    )
    assert report.misconceptions == []
    assert session.query(LearningEvent).one().misconceptions == []


def test_review_mode_emits_nothing(session, user):
    submission = submit(session, user)
    evaluate_submission(
        session, submission.id, user.id,
        provider=FakeExecutionProvider(merged("1\n")),
        explain_runnable=explain_with([]),
    )
    assert session.query(LearningEvent).count() == 0


def test_profiling_failure_does_not_break_the_evaluation(session, user, problem, monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("profiling down")

    monkeypatch.setattr("app.agents.code_eval.nodes.emit_event.ingest", boom)
    submission = submit(session, user, problem.id)
    report = evaluate_submission(
        session, submission.id, user.id,
        provider=FakeExecutionProvider(merged("5\n-7\n")),
        explain_runnable=explain_with([]),
    )
    assert report.evaluation_id is not None
    assert report.tests_passed == 2
