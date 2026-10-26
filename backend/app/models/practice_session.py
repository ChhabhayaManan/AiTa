"""A bounded Practice session: what was served, what was graded, and the wrap-up
feedback generated once when it closes."""

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                              nullable=False, index=True)
    language         = Column(String(10), nullable=False)
    started_at       = Column(DateTime(timezone=True), server_default=func.now(),
                              nullable=False)
    last_activity_at = Column(DateTime(timezone=True), server_default=func.now(),
                              nullable=False)
    ended_at         = Column(DateTime(timezone=True), nullable=True)
    # finished, idle or language_switch.
    end_reason       = Column(String(16), nullable=True)
    graded_count     = Column(Integer, nullable=False, default=0, server_default="0")
    # [{"type": "mcq"|"debug"|"coding", "id": int, "solved": bool}, ...]
    served           = Column(JSON, nullable=False, default=list)
    wrap_up_seen_at  = Column(DateTime(timezone=True), nullable=True)
    # {"summary": str, "work_on_next": [str]}
    feedback         = Column(JSON, nullable=True)
    # none, ready, unavailable or blocked.
    feedback_status  = Column(String(12), nullable=False, default="none",
                              server_default="none")
