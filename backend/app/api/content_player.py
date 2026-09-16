# from fastapi import APIRouter, Depends, status
# from sqlalchemy.orm import Session
# from typing import List

# from app.core.database import get_db
# from app.core.dependencies import get_current_active_user
# from app.models.user import User
# from app.schemas.content_player import (
#     CreateSessionRequest, SessionSummary, SessionDetail,
#     ChatRequest, ChatResponse, MessageFeedbackRequest
# )
# from app.services.content_player_service import ContentPlayerService

# router = APIRouter(prefix="/content-player", tags=["Content Player Agent"])


# # ─── Session management ───────────────────────────────────────────────────────

# @router.post(
#     "/sessions",
#     response_model=SessionSummary,
#     status_code=status.HTTP_201_CREATED,
#     summary="Create a new learning session",
# )
# def create_session(
#     req: CreateSessionRequest,
#     current_user: User = Depends(get_current_active_user),
#     db: Session = Depends(get_db),
# ):
#     """
#     Start a new Content Player session.
#     Choose a mode: qa | code_help | brainstorm | quiz | walkthrough
#     """
#     return ContentPlayerService.create_session(db, current_user.id, req)


# @router.get(
#     "/sessions",
#     response_model=List[SessionSummary],
#     summary="List my learning sessions",
# )
# def list_sessions(
#     current_user: User = Depends(get_current_active_user),
#     db: Session = Depends(get_db),
# ):
#     return ContentPlayerService.get_sessions(db, current_user.id)


# @router.get(
#     "/sessions/{session_id}",
#     response_model=SessionDetail,
#     summary="Get a session with full message history",
# )
# def get_session(
#     session_id: int,
#     current_user: User = Depends(get_current_active_user),
#     db: Session = Depends(get_db),
# ):
#     return ContentPlayerService.get_session(db, session_id, current_user.id)


# @router.delete(
#     "/sessions/{session_id}",
#     summary="Archive a session",
# )
# def archive_session(
#     session_id: int,
#     current_user: User = Depends(get_current_active_user),
#     db: Session = Depends(get_db),
# ):
#     ContentPlayerService.archive_session(db, session_id, current_user.id)
#     return {"success": True, "message": "Session archived."}


# # ─── Chat ─────────────────────────────────────────────────────────────────────

# @router.post(
#     "/sessions/{session_id}/chat",
#     response_model=ChatResponse,
#     summary="💬 Send message to Content Player Agent",
# )
# def chat(
#     session_id: int,
#     req: ChatRequest,
#     current_user: User = Depends(get_current_active_user),
#     db: Session = Depends(get_db),
# ):
#     """
#     Send a message (with optional code + error) to the Content Player Agent.
#     The agent will respond based on the session mode:
#     - **qa**: explanation with Socratic follow-ups
#     - **code_help**: debug hints without giving solutions
#     - **brainstorm**: explore approaches and trade-offs
#     - **quiz**: adaptive question-answer testing
#     - **walkthrough**: step-by-step guided learning
#     """
#     return ContentPlayerService.chat(db, session_id, current_user.id, req)


# # ─── Message feedback ─────────────────────────────────────────────────────────

# @router.patch(
#     "/messages/{message_id}/feedback",
#     summary="Rate an agent response (thumbs up/down)",
# )
# def rate_message(
#     message_id: int,
#     req: MessageFeedbackRequest,
#     current_user: User = Depends(get_current_active_user),
#     db: Session = Depends(get_db),
# ):
#     ContentPlayerService.rate_message(db, message_id, current_user.id, req)
#     return {"success": True, "message": "Feedback recorded."}

"""
api/content_player.py — UPDATED with:
  1. Difficulty level stored in session, adjusted per message
  2. Topic sync — if topic changes, updates session + learning profile  
  3. Interested topics from user profile passed to agent

Copy to: backend/app/api/content_player.py
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.exceptions import LLMUnavailable, SessionNotFound
from app.models.user import User
from app.models.content_player import ContentPlayerSession, ContentPlayerMessage
from app.schemas.content_player import (
    SessionCreate, SessionResponse, ChatRequest, ChatResponse, MessageFeedback,
    GenerateProblemRequest, GenerateProblemResponse
)
from app.schemas.problem import ProblemSummary
from app.services.problems import generation
from app.services.problems.listing import to_summary
from app.services.problems.picker import pick_problem, resolve_difficulty
from app.agents.content_player.graph import run_chat_turn

router = APIRouter(prefix="/content-player", tags=["Content Player"])


# ─── Session Management ───────────────────────────────────────────────────────

@router.post("/sessions", response_model=SessionResponse, status_code=201)
async def create_session(
    body: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = ContentPlayerSession(
        user_id=current_user.id,
        mode=body.mode,
        topic=body.topic,
        language=body.language or "python",
        difficulty=body.difficulty or "medium",  # ← store difficulty in session
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/sessions")
def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sessions = (
        db.query(ContentPlayerSession)
        .filter(
            ContentPlayerSession.user_id == current_user.id,
            ContentPlayerSession.is_archived == False,
        )
        .order_by(ContentPlayerSession.created_at.desc())
        .limit(20)
        .all()
    )
    return sessions


@router.get("/sessions/{session_id}")
def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = db.query(ContentPlayerSession).filter(
        ContentPlayerSession.id == session_id,
        ContentPlayerSession.user_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(404, "Session not found")
    
    messages = (
        db.query(ContentPlayerMessage)
        .filter(ContentPlayerMessage.session_id == session_id)
        .order_by(ContentPlayerMessage.created_at.asc())
        .all()
    )
    return {"session": session, "messages": messages}


@router.delete("/sessions/{session_id}")
def archive_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = db.query(ContentPlayerSession).filter(
        ContentPlayerSession.id == session_id,
        ContentPlayerSession.user_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(404, "Session not found")
    session.is_archived = True
    db.commit()
    return {"message": "Session archived"}


# ─── Chat (Main Agent Endpoint) ───────────────────────────────────────────────

@router.post("/sessions/{session_id}/chat", response_model=ChatResponse)
def chat(
    session_id: int,
    body: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """One turn with the tutor.

    Plain `def` on purpose: the graph blocks on the model, so FastAPI must run it in
    a worker thread rather than on the event loop.
    """
    # The graph raises ValueError for an empty message too, so a direct caller is
    # still safe; checked here as well because only the boundary knows that an empty
    # message is 422 while an unreachable session is 404.
    if not body.message.strip():
        raise HTTPException(422, "Message cannot be empty")

    try:
        turn = run_chat_turn(db, session_id, current_user.id, body.message,
                             body.code_snippet)
    except SessionNotFound:
        # Only this. Catching ValueError here would report any internal fault — a bad
        # state validation, a malformed stored column — as a session the student can
        # see but the server claims not to have, and nothing would ever be raised
        # loudly enough to be investigated.
        raise HTTPException(404, "Session not found")
    except LLMUnavailable as exc:
        # The student's message is already saved; nothing was invented in place of a
        # reply, so they are told plainly to try again.
        raise HTTPException(503, exc.detail)

    return ChatResponse(
        message_id=turn.message_id,
        response=turn.reply,
        concepts=turn.concepts,
        mode=turn.mode,
        topic=turn.topic,
        difficulty=turn.difficulty,
        difficulty_changed=turn.difficulty_changed,
        topic_changed=turn.topic_changed,
        comfort_signal=turn.comfort_signal,
        tokens_used=turn.tokens_used,
        follow_up_suggestions=turn.suggestions,
        question_solved=turn.question_solved,
        difficulty_increased=turn.difficulty_increased,
        problem_id=turn.problem_id,
        problem_origin=turn.problem_origin,
    )


# ─── Message Feedback ─────────────────────────────────────────────────────────

@router.patch("/messages/{message_id}/feedback")
def update_feedback(
    message_id: int,
    body: MessageFeedback,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    msg = db.query(ContentPlayerMessage).filter(
        ContentPlayerMessage.id == message_id
    ).first()
    if not msg:
        raise HTTPException(404, "Message not found")
    msg.was_helpful = body.was_helpful
    db.commit()
    return {"message": "Feedback saved"}


# ─── Serve a problem: the bank first, generation only on a miss ───────────────

# Every problem is graded through the same harness, so every skeleton does the same
# thing: read the test count, then solve one block at a time. Only the languages the
# sandbox can compile and run get one — anything else would be graded in review mode.
STARTER_CODE = {
    "python": """import sys


def solve():
    # Read this test case's input and print its answer.
    pass


for _ in range(int(sys.stdin.readline())):
    solve()
""",
    "cpp": """#include <bits/stdc++.h>
using namespace std;

void solve() {
    // Read this test case's input and print its answer.
}

int main() {
    int t;
    cin >> t;
    while (t--) solve();
    return 0;
}
""",
}

DEFAULT_STARTER_LANGUAGE = "python"


def starter_code_for(language: str | None) -> str:
    return STARTER_CODE.get(
        (language or "").strip().lower(), STARTER_CODE[DEFAULT_STARTER_LANGUAGE]
    )


def _to_response(
    summary: ProblemSummary,
    *,
    origin: str,
    language: str | None = None,
    title: str | None = None,
    hints: list | None = None,
) -> GenerateProblemResponse:
    examples = []
    if summary.sample_input is not None:
        examples.append({
            "input": summary.sample_input,
            "output": summary.sample_output,
            "explanation": "One worked example, in the exact shape your program is run with.",
        })
    return GenerateProblemResponse(
        problem_id=summary.id,
        origin=origin,
        # The difficulty the problem has, never the one that was asked for.
        difficulty=summary.difficulty or "",
        title=title or summary.title,
        description=summary.statement,
        examples=examples,
        constraints=[c.strip() for c in (summary.constraints or "").splitlines() if c.strip()],
        hints=hints or [],
        starter_code=starter_code_for(language),
    )


@router.post("/generate-problem", response_model=GenerateProblemResponse)
def generate_problem(
    body: GenerateProblemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Serve a curated problem when the bank has one, otherwise generate a real one.

    Plain `def` on purpose: the generation path is synchronous and blocking, so
    FastAPI must run it in a worker thread rather than on the event loop.
    """
    # Resolved once, at the boundary, so the pick and the generation agree on it.
    difficulty = resolve_difficulty(body.difficulty)

    picked = pick_problem(
        db,
        topic=body.topic,
        difficulty=difficulty,
        exclude_ids=body.exclude_ids,
    )
    if picked is not None:
        return _to_response(to_summary(picked), origin="bank", language=body.language)

    try:
        result = generation.generate_problem(db, topic=body.topic,
                                             difficulty=difficulty)
    except LLMUnavailable:
        raise HTTPException(503, "A problem could not be generated right now. "
                                 "Please try again in a moment.")

    if result.ungradeable_reason:
        # The row survives for a later attempt, but an ungradeable problem is not
        # something to put in front of a student.
        raise HTTPException(503, "A problem was written but no test cases could be "
                                 "verified for it. Please try again.")

    return _to_response(to_summary(result.problem), origin="generated",
                        language=body.language, title=result.title, hints=result.hints)
