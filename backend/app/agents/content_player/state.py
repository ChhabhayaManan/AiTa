from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ChatState(BaseModel):
    """Pipeline state for one Content Player chat turn."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    db: Any
    session_id: int
    user_id: int
    message: str
    code_snippet: Optional[str] = None

    # Injection point. None in production; tests supply a fake so the graph runs
    # with no network.
    respond_runnable: Any = None

    # load_session
    session: Any = None
    user: Any = None
    history: list[dict] = []
    mode: str = "qa"
    topic: str = ""
    language: str = "python"
    skill_level: str = "beginner"
    interested_topics: list[str] = []
    difficulty: str = "medium"
    consecutive_easy_solves: int = 0
    solved_questions: list[int] = []

    # detect_signals
    comfort_signal: str = "comfortable"
    accuracy: Optional[float] = None
    question_solved: bool = False
    difficulty_increased: bool = False
    new_difficulty: str = "medium"
    new_consecutive: int = 0
    topic_changed: bool = False
    effective_topic: str = ""

    # select_problem
    problem_id: Optional[int] = None
    problem_statement: Optional[str] = None
    problem_origin: Optional[str] = None

    # respond
    reply: Optional[str] = None
    concepts: list[str] = []
    mastery: list[str] = []
    weak: list[str] = []
    suggestions: list[str] = []
    tokens_used: int = 0
    latency_ms: int = 0
    model_used: Optional[str] = None
    # The one thing this agent cannot degrade around: with no reply there is no turn.
    llm_failed: bool = False

    # persist
    turn: Any = None
