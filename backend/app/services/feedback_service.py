from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.agents.feedback.graph import generate_feedback
from app.models.feedback import FeedbackTone
from app.schemas.feedback import GenerateFeedbackRequest
from app.services.feedback import reports


class FeedbackService:

    @staticmethod
    def generate(db: Session, user_id: int, req: GenerateFeedbackRequest):
        if not req.evaluation_id and not req.cp_session_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Provide at least one of evaluation_id or cp_session_id."
            )
        try:
            tone = FeedbackTone(req.tone) if isinstance(req.tone, str) else req.tone
            return generate_feedback(
                db, user_id, req.evaluation_id, req.cp_session_id, tone
            )
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except RuntimeError as e:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))

    @staticmethod
    def get_reports(db: Session, user_id: int):
        return reports.get_reports(db, user_id)

    @staticmethod
    def get_report(db: Session, report_id: int, user_id: int):
        try:
            return reports.get_report(db, report_id, user_id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @staticmethod
    def mark_read(db: Session, report_id: int, user_id: int):
        reports.mark_read(db, report_id, user_id)

    @staticmethod
    def unread_count(db: Session, user_id: int) -> int:
        return reports.unread_count(db, user_id)
