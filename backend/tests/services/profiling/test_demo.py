import pytest

from app.agents.profiling.graph import ingest
from app.models.code_eval import CodeEvaluation, CodeSubmission, Language
from app.models.learning import HintEvent, LearningEvent, TopicMastery
from app.models.problem import Problem, ProblemSource
from app.models.user import User
from app.services.profiling.demo import report, reset_account
from app.services.profiling.service import EventInput


@pytest.fixture
def other(session):
    u = User(email="keep@example.com", username="keep", hashed_password="x")
    session.add(u)
    session.commit()
    ingest(session, EventInput(user_id=u.id, kind="code", score=1.0, raw_topic="loops"))
    return u


def test_reset_clears_only_the_named_account(session, other):
    demo = reset_account(session, "demo@example.com", "demo", "DemoPass123!")
    ingest(session, EventInput(user_id=demo.id, kind="code", score=0.5, raw_topic="loops"))

    fresh = reset_account(session, "demo@example.com", "demo", "DemoPass123!")

    assert session.query(LearningEvent).filter_by(user_id=fresh.id).count() == 0
    assert session.query(TopicMastery).filter_by(user_id=fresh.id).count() == 0
    assert session.query(LearningEvent).filter_by(user_id=other.id).count() == 1
    assert session.query(User).filter_by(email="demo@example.com").count() == 1


def test_report_numbers(session, other):
    problem = Problem(source=ProblemSource.DSA, statement="s", statement_hash="r" * 64)
    session.add(problem)
    submission = CodeSubmission(user_id=other.id, language=Language.PYTHON, code="x", title="t")
    session.add(submission)
    session.flush()
    for status in ("verified", "verified", "unverified"):
        session.add(CodeEvaluation(submission_id=submission.id, user_id=other.id,
                                   verification_status=status, status="done"))
    session.add_all([
        HintEvent(user_id=other.id, problem_id=problem.id, level=1, was_blocked=False),
        HintEvent(user_id=other.id, problem_id=problem.id, level=2, was_blocked=True),
        HintEvent(user_id=other.id, problem_id=problem.id, level=3, was_blocked=False),
    ])
    session.commit()

    numbers = report(session, other.id)

    assert numbers["hint_leak_rate"] == {"blocked": 1, "llm_hints": 2, "rate": 0.5}
    assert numbers["correctness"] == {"verified": 2, "unverified": 1}
    assert numbers["mastery_trace"]["loops"] == [
        {"kind": "code", "score": 1.0, "hint": 0, "before": 0.3, "after": 0.51}]
