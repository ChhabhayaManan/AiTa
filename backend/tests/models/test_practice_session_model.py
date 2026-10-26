from app.models.learning import LearningEvent
from app.models.practice_session import PracticeSession
from app.models.user import User


def test_session_roundtrip(session):
    u = User(email="ps@example.com", username="psuser", hashed_password="x")
    session.add(u)
    session.flush()
    s = PracticeSession(user_id=u.id, language="c",
                        served=[{"type": "mcq", "id": 1, "solved": False}])
    session.add(s)
    session.flush()
    session.add(LearningEvent(user_id=u.id, kind="mcq", item_id=1, score=1.0, weight=1.0,
                              language="c", session_id=s.id))
    session.commit()
    session.expire_all()

    assert s.feedback_status == "none"
    assert s.graded_count == 0
    assert s.served == [{"type": "mcq", "id": 1, "solved": False}]
    assert session.query(LearningEvent).one().session_id == s.id
