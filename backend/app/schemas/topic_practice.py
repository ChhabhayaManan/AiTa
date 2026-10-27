from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.schemas.gamification import AwardOut


class ExplanationOut(BaseModel):
    topic: str
    language: str
    markdown: str


class RunOut(BaseModel):
    session_id: int
    total: int


class RunStepOut(BaseModel):
    session_id: int
    position: int
    total: int
    done: bool
    item_type: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    item: Optional[Dict[str, Any]] = None


class TheoryAnswerRequest(BaseModel):
    answer: str = Field("", max_length=2000)


class TheoryAnswerOut(BaseModel):
    score: float
    key_points: List[str]
    points_present: List[bool]
    model_answer: str
    feedback: str
    mastery_after: Optional[float] = None
    awards: List[AwardOut] = []
