import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.dependencies import get_current_active_user
from app.models.learning import McqQuestion
from app.models.user import User


@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False},
                           poolclass=StaticPool)
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    user = User(email="api-a@example.com", username="apia", hashed_password="x")
    db.add(user)
    db.add(McqQuestion(external_id="diag-loops", topic="loops", difficulty="easy",
                       stem="What does print(len(range(1, 5))) print?",
                       options=[{"text": "5", "misconception": "off_by_one"},
                                {"text": "4", "misconception": None}],
                       answer_index=1, verify_code="print(len(range(1, 5)))",
                       explanations=["range stops before its end"],
                       is_diagnostic=True, reviewed=True))
    db.commit()

    from app.main import app
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_active_user] = lambda: user
    yield TestClient(app), db
    app.dependency_overrides.clear()
    db.close()


def test_next_then_answer_round_trip(client):
    http, _ = client
    nxt = http.get("/api/v1/assessment/next")
    assert nxt.status_code == 200
    body = nxt.json()
    assert body["item_type"] == "diagnostic"
    assert "answer_index" not in body["item"] and "verify_code" not in nxt.text

    answer = http.post(f"/api/v1/assessment/mcq/{body['item']['id']}/answer",
                       json={"chosen_index": 0})
    assert answer.status_code == 200
    result = answer.json()
    assert result["correct"] is False
    assert result["misconception"] == "off_by_one"
    assert result["answer_index"] == 1

    mastery = http.get("/api/v1/profile/mastery").json()
    loops = next(t for t in mastery["topics"] if t["topic"] == "loops")
    assert loops["evidence_count"] == 1


def test_unknown_question_is_404_and_bad_index_422(client):
    http, _ = client
    assert http.post("/api/v1/assessment/mcq/999/answer",
                     json={"chosen_index": 0}).status_code == 404
    assert http.post("/api/v1/assessment/mcq/1/answer",
                     json={"chosen_index": 9}).status_code == 422


def test_nothing_to_serve_is_503(client, monkeypatch):
    from app.core.exceptions import LLMUnavailable
    from app.services.assessment import policy

    def refuse(*a, **k):
        raise LLMUnavailable("generation is stubbed in tests")

    monkeypatch.setattr(policy, "generate_problem", refuse)
    http, db = client
    db.query(McqQuestion).delete()
    db.commit()

    assert http.get("/api/v1/assessment/next").status_code == 503
