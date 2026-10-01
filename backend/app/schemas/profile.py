from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class TopicMasteryOut(BaseModel):
    topic: str
    label: str
    mastery: float
    evidence_count: int
    confidence: float
    band: str
    last_event_at: Optional[datetime] = None
    prerequisites: List[str]
    unlocked: bool


class MisconceptionCount(BaseModel):
    tag: str
    count: int


class LearningEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    kind: str
    item_id: Optional[int] = None
    topic: Optional[str] = None
    raw_topic: Optional[str] = None
    score: float
    weight: float
    hint_level_used: int
    misconceptions: List[str] = []
    mastery_before: Optional[float] = None
    mastery_after: Optional[float] = None
    source_ref: Optional[str] = None
    created_at: Optional[datetime] = None


class MasteryResponse(BaseModel):
    topics: List[TopicMasteryOut]
    top_misconceptions: List[MisconceptionCount]
    hint_reliance: float
    recent_events: List[LearningEventOut]
