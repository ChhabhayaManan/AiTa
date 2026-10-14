from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.gamification import GamificationSummary
from app.services.gamification.service import summary

router = APIRouter(prefix="/gamification", tags=["Gamification"])


@router.get("/me", response_model=GamificationSummary,
            summary="Your points, topic levels, badges and last-7-days self-board")
def get_mine(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return summary(db, current_user.id)
