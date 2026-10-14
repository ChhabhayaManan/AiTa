from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.schemas.gamification import AwardOut


class NextItemResponse(BaseModel):
    item_type: str
    topic: str
    difficulty: str
    item: Dict[str, Any]
    reason: str


class McqAnswerRequest(BaseModel):
    chosen_index: int


class McqAnswerResponse(BaseModel):
    correct: bool
    chosen_index: int
    answer_index: int
    misconception: Optional[str] = None
    explanation: Optional[str] = None
    mastery_after: Optional[float] = None
    awards: List[AwardOut] = []


class DebugSubmitRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=50000)


class DebugSubmitResponse(BaseModel):
    fixed: bool
    verdict: str
    tests_passed: int
    tests_total: int
    failing_input: Optional[str] = None
    failing_expected: Optional[str] = None
    failing_actual: Optional[str] = None
    mastery_after: Optional[float] = None
    awards: List[AwardOut] = []
