from app.agents.content_player.state import ChatState
from app.core.exceptions import SessionNotFound
from app.models.content_player import ContentPlayerMessage, ContentPlayerSession
from app.models.user import User


def _role(message: ContentPlayerMessage) -> str:
    return message.role if isinstance(message.role, str) else message.role.value


def _problem_ids(values) -> list[int]:
    """`solved_questions` holds problem ids now, but sessions that ran before this
    migration hold `_question_key` strings like "arrays_easy" instead.

    Those name no problem, so they are dropped rather than carried: a legacy entry
    matches nothing, which is what excluding it was always meant to mean. Keeping
    them would fail state validation on every turn and strand the session.
    """
    ids = []
    for value in values or []:
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            ids.append(value)
        # isdecimal, not isdigit: "²" is a digit that int() refuses.
        elif isinstance(value, str) and value.strip().isdecimal():
            ids.append(int(value.strip()))
    return ids


def load_session(state: ChatState) -> ChatState:
    if not state.message.strip():
        raise ValueError("Message cannot be empty.")

    session = (
        state.db.query(ContentPlayerSession)
        .filter(
            ContentPlayerSession.id == state.session_id,
            ContentPlayerSession.user_id == state.user_id,
        )
        .first()
    )
    if session is None:
        raise SessionNotFound("Session not found.")

    user = state.db.query(User).filter(User.id == state.user_id).first()

    messages = (
        state.db.query(ContentPlayerMessage)
        .filter(ContentPlayerMessage.session_id == state.session_id)
        .order_by(ContentPlayerMessage.created_at.asc())
        .all()
    )

    state.session = session
    state.user = user
    state.history = [{"role": _role(m), "content": m.content} for m in messages]
    state.mode = session.mode if isinstance(session.mode, str) else session.mode.value
    state.topic = session.topic or ""
    state.language = session.language or "python"
    state.difficulty = session.difficulty or "medium"
    state.consecutive_easy_solves = session.consecutive_easy_solves or 0
    state.solved_questions = _problem_ids(session.solved_questions)

    if user is not None:
        state.interested_topics = user.interested_topics or []
        state.skill_level = (user.skill_level.value
                             if getattr(user.skill_level, "value", None)
                             else (user.skill_level or "beginner"))
    return state
