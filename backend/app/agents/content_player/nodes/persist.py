from datetime import datetime, timezone

from app.agents.content_player.schemas import ChatTurn
from app.agents.content_player.state import ChatState
from app.models.content_player import ContentPlayerMessage


def _union(existing, new) -> list:
    """Set semantics, stable order — the signals are shown to the student and read
    back by the Feedback Agent, so they should not reshuffle on every turn."""
    merged = list(existing or [])
    for item in new or []:
        if item not in merged:
            merged.append(item)
    return merged


def _sync_topic(state: ChatState) -> None:
    """A topic the student actually moved to follows them into the session and onto
    what they are known to be studying. The learner profile is the Profiling Agent's;
    chat is not graded evidence, so nothing here writes it."""
    session, user = state.session, state.user
    topic = state.effective_topic
    session.topic = topic

    if user is not None:
        topics = user.interested_topics or []
        if topic not in topics:
            user.interested_topics = topics + [topic]


def persist(state: ChatState) -> ChatState:
    db, session = state.db, state.session

    session.last_message_at = datetime.now(timezone.utc)

    db.add(ContentPlayerMessage(
        session_id=state.session_id,
        user_id=state.user_id,
        role="user",
        content=state.message,
        has_code=bool(state.code_snippet),
        code_snippet=state.code_snippet,
    ))

    if state.llm_failed:
        # The student's turn is kept so nothing they wrote is lost, but no assistant
        # message is written: there is no reply to write, and a made-up one would be
        # worse than none.
        #
        # Nothing else is applied either. The student is told to try again, and this
        # turn's signals — difficulty, the solve streak, the topic switch, confusion —
        # would then be counted a second time off the message they resend. They are
        # left to the turn that actually completes, the same reasoning that holds the
        # served problem id back.
        session.total_messages = (session.total_messages or 0) + 1
        db.commit()
        return state

    if state.topic_changed and state.effective_topic:
        _sync_topic(state)

    session.difficulty = state.new_difficulty
    session.consecutive_easy_solves = state.new_consecutive

    assistant = ContentPlayerMessage(
        session_id=state.session_id,
        user_id=state.user_id,
        role="assistant",
        content=state.reply,
        tokens_used=state.tokens_used,
        latency_ms=state.latency_ms,
        model_used=state.model_used,
    )
    db.add(assistant)

    session.concepts_covered = _union(session.concepts_covered, state.concepts)
    session.mastery_signals = _union(session.mastery_signals, state.mastery)
    session.weak_signals = _union(session.weak_signals, state.weak)
    if state.comfort_signal == "struggling":
        session.confusion_detected = True
    session.total_messages = (session.total_messages or 0) + 2
    session.total_tokens_used = (session.total_tokens_used or 0) + state.tokens_used
    if state.model_used:
        session.agent_model = state.model_used

    if state.problem_id is not None and state.problem_id not in state.solved_questions:
        # The student has now been set this problem, so the next turn must not pick
        # it again. Nothing wrote this column before, which is why every session kept
        # being offered the same first problem.
        session.solved_questions = state.solved_questions + [state.problem_id]

    db.commit()
    db.refresh(assistant)

    state.turn = ChatTurn(
        message_id=assistant.id,
        reply=state.reply,
        mode=state.mode,
        topic=session.topic,
        difficulty=state.new_difficulty,
        comfort_signal=state.comfort_signal,
        concepts=state.concepts,
        suggestions=state.suggestions,
        difficulty_changed=(state.new_difficulty != state.difficulty
                            or state.difficulty_increased),
        topic_changed=state.topic_changed,
        tokens_used=state.tokens_used,
        question_solved=state.question_solved,
        difficulty_increased=state.difficulty_increased,
        problem_id=state.problem_id,
        problem_origin=state.problem_origin,
    )
    return state
