from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel

from app.schemas.gamification import AwardOut


class CurrentOut(BaseModel):
    id: Optional[int] = None
    graded_count: int = 0


class PendingOut(BaseModel):
    id: int
    ended_at: datetime
    end_reason: str
    solved: int
    topics: List[str]


class TypeCountOut(BaseModel):
    tried: int
    solved: int


class TopicChangeOut(BaseModel):
    topic: str
    before: float
    after: float
    band_after: str


class MistakeOut(BaseModel):
    misconception: str
    count: int


class SessionFeedbackOut(BaseModel):
    summary: str
    work_on_next: List[str] = []


class FeedbackRequest(BaseModel):
    retry: bool = False


class WrapUpOut(BaseModel):
    id: int
    language: str
    started_at: datetime
    ended_at: datetime
    end_reason: str
    # Set for a topic run: the one topic the student chose.
    topic: Optional[str] = None
    duration_s: int
    by_type: Dict[str, TypeCountOut]
    topics: List[TopicChangeOut]
    hints: Dict[int, int]
    mistakes: List[MistakeOut]
    stuck_topics: List[str]
    awards: Optional[List[AwardOut]] = None
    feedback: Optional[SessionFeedbackOut] = None
    feedback_status: str
