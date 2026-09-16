"""HTTP-level wiring for POST /content-player/generate-problem.

Proves the bank is asked first, that both paths serialise through FastAPI with no
answer material on them, and that neither outage reaches the student as raw
infrastructure text.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.agents.code_eval.schemas import GeneratedCase, GeneratedTests
from app.agents.content_player.schemas import TutorReply
from app.core.database import Base, get_db
from app.core.dependencies import get_current_active_user, get_current_user
from app.core.exceptions import ExecutorUnavailable
from app.models.content_player import ContentPlayerMessage, ContentPlayerSession
from app.models.problem import (
    Difficulty,
    IOMode,
    Problem,
    ProblemSource,
    TestCase,
    TestCaseKind,
    TestCaseOrigin,
)
from app.models.user import User
from app.services.execution.base import ExecResult, ExecStatus
from app.services.problems.schemas import ProblemDraft
from tests.conftest import FakeExecutionProvider

ENDPOINT = "/api/v1/content-player/generate-problem"
CHAT = "/api/v1/content-player/sessions/{id}/chat"
REFERENCE = "print(sum(map(int, input().split())))"


@pytest.fixture
def client():
    # StaticPool keeps every connection on the same in-memory database; TestClient
    # runs the request on another thread, which would otherwise get an empty one.
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()

    user = User(email="cp@example.com", username="cpuser", hashed_password="x")
    db.add(user)
    db.commit()

    from app.main import app

    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_current_active_user] = lambda: user

    # Constructed without `with`, so the lifespan never runs against the real database.
    yield TestClient(app), db

    app.dependency_overrides.clear()
    db.close()


def seed_curated(db, topic="arrays", difficulty=Difficulty.EASY):
    problem = Problem(
        source=ProblemSource.DSA, external_id="dsa-two-sum",
        statement="Read two integers and print their sum.", statement_hash="a" * 64,
        topic=topic, difficulty=difficulty, io_mode=IOMode.STDIN_STDOUT,
    )
    db.add(problem)
    db.commit()
    db.add(TestCase(
        problem_id=problem.id, kind=TestCaseKind.SAMPLE, stdin="1 2\n",
        expected_stdout="3", stdin_hash="b" * 64,
        origin=TestCaseOrigin.CROSS_CHECKED, ordinal=1,
    ))
    db.commit()
    return problem


def fake_statement(monkeypatch, draft=None, parsed=True):
    """Stand in for the structured statement call, without building a model."""
    draft = draft or ProblemDraft(
        title="Sum Two Integers",
        statement="Read two integers on one line and print their sum.",
        constraints=["1 <= a <= 100"],
        hints=["Splitting a line", "The two values always fit in an int"],
    )

    class Fake:
        def invoke(self, prompt):
            return {"parsed": draft if parsed else None, "raw": None}

    monkeypatch.setattr("app.services.problems.generation.get_chat_model",
                        lambda **kwargs: None)
    monkeypatch.setattr("app.services.problems.generation.structured",
                        lambda model, schema: Fake())


def fake_tests(monkeypatch, provider):
    """Drive the real generate_tests through its module-level default generator."""
    generated = GeneratedTests(
        reference_solution=REFERENCE,
        cases=[GeneratedCase(kind="normal", stdin=s, expected_stdout=e, rationale="r")
               for s, e in (("1 2\n", "3"), ("4 5\n", "9"), ("0 0\n", "0"))],
    )
    monkeypatch.setattr(
        "app.services.test_generation.generate_tests._default_generator",
        lambda **kwargs: generated,
    )
    monkeypatch.setattr("app.services.execution.run_code.get_provider",
                        lambda: provider)


def ok(stdout):
    return ExecResult(status=ExecStatus.OK, stdout=stdout, time_ms=1)


def test_bank_is_asked_before_anything_is_generated(client, monkeypatch):
    test_client, db = client
    problem = seed_curated(db)

    def explode(*args, **kwargs):
        raise AssertionError("generation must not run on a bank hit")

    monkeypatch.setattr("app.services.problems.generation.generate_problem", explode)

    response = test_client.post(ENDPOINT, json={"topic": "arrays",
                                                "difficulty": "easy"})

    assert response.status_code == 200
    body = response.json()
    assert body["origin"] == "bank"
    assert body["problem_id"] == problem.id
    assert body["difficulty"] == "easy"
    assert body["title"] == "Two Sum"
    assert body["examples"]


def test_bank_miss_generates_a_real_problem(client, monkeypatch):
    test_client, db = client
    seed_curated(db, topic="arrays")
    fake_statement(monkeypatch)
    fake_tests(monkeypatch, FakeExecutionProvider([ok("3\n"), ok("9\n"), ok("0\n")]))

    response = test_client.post(ENDPOINT, json={"topic": "graphs",
                                                "difficulty": "medium"})

    assert response.status_code == 200
    body = response.json()
    assert body["origin"] == "generated"
    assert body["title"] == "Sum Two Integers"
    assert body["difficulty"] == "medium"

    stored = db.query(Problem).filter(Problem.id == body["problem_id"]).one()
    assert stored.source is ProblemSource.GENERATED
    assert len(stored.test_cases) == 3


@pytest.mark.parametrize("topic", ["arrays", "graphs"])
def test_neither_path_returns_answer_material(client, monkeypatch, topic):
    test_client, db = client
    seed_curated(db, topic="arrays")
    fake_statement(monkeypatch)
    fake_tests(monkeypatch, FakeExecutionProvider([ok("3\n"), ok("9\n"), ok("0\n")]))

    response = test_client.post(ENDPOINT, json={"topic": topic,
                                                "difficulty": "easy"})

    assert response.status_code == 200
    body = response.json()
    assert body["solution_code"] == ""
    assert body["explanation"] == ""
    assert REFERENCE not in response.text


def test_hints_are_capped_on_the_wire(client, monkeypatch):
    test_client, db = client
    fake_statement(monkeypatch, draft=ProblemDraft(
        title="Sum Two Integers",
        statement="Read two integers on one line and print their sum.",
        constraints=[],
        hints=["A running sum", "The order never matters",
               "Add each element as you pass it", "Print once at the end"],
    ))
    fake_tests(monkeypatch, FakeExecutionProvider([ok("3\n"), ok("9\n"), ok("0\n")]))

    response = test_client.post(ENDPOINT, json={"topic": "graphs"})

    assert response.status_code == 200
    assert response.json()["hints"] == ["A running sum", "The order never matters"]


def test_expert_is_served_and_labelled_as_hard(client, monkeypatch):
    test_client, db = client
    seed_curated(db, topic="arrays", difficulty=Difficulty.HARD)

    response = test_client.post(ENDPOINT, json={"topic": "arrays",
                                                "difficulty": "expert"})

    assert response.status_code == 200
    assert response.json()["difficulty"] == "hard"


def test_statement_outage_is_a_plain_503(client, monkeypatch):
    test_client, _ = client
    fake_statement(monkeypatch, parsed=False)

    response = test_client.post(ENDPOINT, json={"topic": "graphs"})

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "A problem could not be generated right now. Please try again in a moment."
    )


def test_executor_outage_is_a_plain_503_not_infrastructure_text(client, monkeypatch):
    test_client, db = client
    fake_statement(monkeypatch)

    class Exploding(FakeExecutionProvider):
        def __init__(self):
            super().__init__([])

        def run_batch(self, language, source, stdins, limits):
            raise ExecutorUnavailable(
                "executor unreachable: [Errno 11001] getaddrinfo failed"
            )

    fake_tests(monkeypatch, Exploding())

    response = test_client.post(ENDPOINT, json={"topic": "graphs"})

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert detail == ("A problem was written but no test cases could be verified "
                      "for it. Please try again.")
    assert "getaddrinfo" not in response.text
    assert "executor" not in response.text

    # 4a.2(4): the row survives the outage so a later attempt reuses it.
    assert db.query(Problem).filter(
        Problem.source == ProblemSource.GENERATED).count() == 1


# ─── The chat turn ───────────────────────────────────────────────────────────

def seed_chat_session(db, topic="recursion", mode="qa"):
    user = db.query(User).one()
    cp = ContentPlayerSession(user_id=user.id, mode=mode, topic=topic,
                              language="python", difficulty="medium")
    db.add(cp)
    db.commit()
    return cp


class TutorError(Exception):
    """No rate-limit marker in the text, so no retry sleeps."""


def fake_tutor(monkeypatch, error=None):
    """Stand in for the structured tutor call, without building a model."""
    parsed = TutorReply(
        reply="Start from the smallest input you can write down.",
        concepts=["recursion"], mastery=[], weak=["call stack"],
        suggestions=["What is the smallest input?"],
    )

    class Fake:
        def invoke(self, payload):
            if error:
                raise error
            return {"parsed": parsed, "raw": None}

    monkeypatch.setattr("app.agents.content_player.nodes.respond.get_chat_model",
                        lambda **kwargs: None)
    monkeypatch.setattr("app.agents.content_player.nodes.respond.structured",
                        lambda model, schema: Fake())


def test_chat_returns_the_turn(client, monkeypatch):
    test_client, db = client
    cp = seed_chat_session(db)
    fake_tutor(monkeypatch)

    response = test_client.post(CHAT.format(id=cp.id),
                                json={"message": "Where do I start with this?"})

    assert response.status_code == 200
    body = response.json()
    assert body["response"] == "Start from the smallest input you can write down."
    assert body["concepts"] == ["recursion"]
    assert body["mode"] == "qa"
    assert body["topic"] == "recursion"
    assert body["difficulty"] == "medium"
    assert body["comfort_signal"] == "comfortable"
    # The name the frontend's follow-up chips have always read.
    assert body["follow_up_suggestions"] == ["What is the smallest input?"]
    assert body["message_id"]
    assert "AGENT_META" not in response.text


def test_chat_is_a_plain_503_when_the_tutor_is_unavailable(client, monkeypatch):
    test_client, db = client
    cp = seed_chat_session(db)
    fake_tutor(monkeypatch, error=TutorError("upstream call failed"))

    response = test_client.post(CHAT.format(id=cp.id),
                                json={"message": "Where do I start with this?"})

    assert response.status_code == 503
    assert "try again" in response.json()["detail"]
    assert "upstream call failed" not in response.text

    # The student's turn is kept; no reply was invented in its place.
    rows = db.query(ContentPlayerMessage).filter(
        ContentPlayerMessage.session_id == cp.id).all()
    assert [r.role for r in rows] == ["user"]


def test_chat_on_an_unknown_session_is_404(client, monkeypatch):
    test_client, _ = client
    fake_tutor(monkeypatch)

    response = test_client.post(CHAT.format(id=4242), json={"message": "Hello?"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_chat_with_an_empty_message_is_422(client, monkeypatch):
    test_client, db = client
    cp = seed_chat_session(db)
    fake_tutor(monkeypatch)

    response = test_client.post(CHAT.format(id=cp.id), json={"message": "   "})

    assert response.status_code == 422


@pytest.mark.parametrize("language, marker", [
    ("python", "import sys"),
    ("cpp", "#include <bits/stdc++.h>"),
])
def test_starter_code_follows_the_requested_language(client, monkeypatch, language, marker):
    test_client, db = client
    seed_curated(db)

    def explode(*args, **kwargs):
        raise AssertionError("generation must not run on a bank hit")

    monkeypatch.setattr("app.services.problems.generation.generate_problem", explode)

    response = test_client.post(ENDPOINT, json={"topic": "arrays",
                                                "difficulty": "easy",
                                                "language": language})

    assert response.status_code == 200
    assert marker in response.json()["starter_code"]


def test_an_unrunnable_language_still_gets_a_usable_starter(client, monkeypatch):
    """The picker offers only cpp and python, but the field is a free string."""
    test_client, db = client
    seed_curated(db)
    monkeypatch.setattr("app.services.problems.generation.generate_problem",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("bank hit")))

    response = test_client.post(ENDPOINT, json={"topic": "arrays",
                                                "difficulty": "easy",
                                                "language": "haskell"})

    assert response.status_code == 200
    assert "import sys" in response.json()["starter_code"]
