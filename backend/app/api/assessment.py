from dataclasses import asdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agents.assessment.graph import next_item
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.assessment import (
    DebugSubmitRequest,
    DebugSubmitResponse,
    McqAnswerRequest,
    McqAnswerResponse,
    NextItemResponse,
)
from app.services.assessment.grading import grade_debug, grade_mcq

router = APIRouter(prefix="/assessment", tags=["Assessment Agent"])


@router.get("/next", response_model=NextItemResponse, summary="What to practise next, and why")
def get_next(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Diagnostic first; then the weakest unlocked topic, with the item type and
    difficulty set by its measured mastery. Coding problems are submitted through
    `/code-eval/evaluate` with their `id` as `problem_id`."""
    return asdict(next_item(db, current_user.id))


@router.post("/mcq/{question_id}/answer", response_model=McqAnswerResponse,
             summary="Answer a multiple-choice question")
def answer_mcq(
    question_id: int,
    req: McqAnswerRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return asdict(grade_mcq(db, current_user.id, question_id, req.chosen_index))


@router.post("/debug/{challenge_id}/submit", response_model=DebugSubmitResponse,
             summary="Submit a fix for a debugging challenge")
def submit_debug(
    challenge_id: int,
    req: DebugSubmitRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return asdict(grade_debug(db, current_user.id, challenge_id, req.code))
