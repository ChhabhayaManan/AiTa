from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.agents.code_eval.schemas import EvalReport
from app.models.code_eval import Language

# The evaluation response and the Month 2 chatbot tool return are the same model.
# One definition means one place a field can leak from, and one place to test.
EvaluationResult = EvalReport


class SubmitCodeRequest(BaseModel):
    language:        Language
    code:            str = Field(..., min_length=1, max_length=50000)
    title:           Optional[str] = Field(None, max_length=300)
    problem_context: Optional[str] = Field(None, max_length=5000)
    expected_output: Optional[str] = Field(None, max_length=2000)
    # Set when the submission answers a stored problem, curated or generated. Binding
    # by id beats sending the statement back: the displayed text carries a preamble the
    # stored one does not, so a round trip through the fingerprint would duplicate it.
    problem_id:      Optional[int] = None


class RunCodeRequest(BaseModel):
    problem_id: int
    language:   Language
    code:       str = Field(..., min_length=1, max_length=50000)


class RunCase(BaseModel):
    input:    str
    expected: str
    actual:   str
    passed:   bool


class RunCodeResult(BaseModel):
    verdict:        str
    status:         str
    compile_output: Optional[str] = None
    stderr:         str = ""
    passed:         int
    total:          int
    cases:          List[RunCase]


class SubmissionSummary(BaseModel):
    id:         int
    title:      Optional[str]
    language:   Language
    problem_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SubmissionDetail(SubmissionSummary):
    code:            str
    problem_context: Optional[str] = None
    expected_output: Optional[str] = None
    # The stored statement plus the batch convention, i.e. what the student must
    # actually satisfy. None when the submission has no problem attached.
    problem_statement: Optional[str] = None

    class Config:
        from_attributes = True


class HistoryPoint(BaseModel):
    eval_number:   int
    overall_score: float
    language:      Language
    submission_id: int
    evaluation_id: int
    created_at:    datetime

    class Config:
        from_attributes = True


class UserEvalStats(BaseModel):
    total_submissions:        int
    total_evaluations:        int
    avg_overall_score:        float
    best_score:               float
    languages_used:           List[str]
    most_common_issues:       List[str]
    improvement_trend:        float
    verified_evaluations:     int = 0
    avg_verified_correctness: Optional[float] = None
    recent_history:           List[HistoryPoint] = []
