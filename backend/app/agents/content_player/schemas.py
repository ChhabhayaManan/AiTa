from dataclasses import dataclass, field
from typing import Optional

from pydantic import BaseModel, Field


class TutorReply(BaseModel):
    """One tutor turn, reply and learning signals together.

    These descriptions are the only instruction the model reads under structured
    output, so they carry what the removed hidden-metadata sentinel block used to ask
    for in prose. There is no `confusion` field: confusion is read out of the
    student's own message by the detectors, never asserted by the model about itself.
    """

    reply: str = Field(
        description="The whole message the student reads, in markdown. Say everything "
                    "here and nowhere else, stay on the session's topic, never hand "
                    "over a complete solution, and end with one question or challenge."
    )
    concepts: list[str] = Field(
        default_factory=list,
        description="Concepts this turn actually covered, named the way a syllabus "
                    "would name them, e.g. 'binary search', 'loop invariants'",
    )
    mastery: list[str] = Field(
        default_factory=list,
        description="Topics the student's own message shows they have understood. "
                    "Empty unless they demonstrated it — this feeds their profile",
    )
    weak: list[str] = Field(
        default_factory=list,
        description="Topics the student's message shows they are struggling with, "
                    "for the same profile",
    )
    suggestions: list[str] = Field(
        default_factory=list,
        description="Two or three follow-up questions the student could ask next, "
                    "each one a whole question they could send as-is",
    )


@dataclass(frozen=True)
class ChatTurn:
    """The result of one completed chat turn, as the endpoint needs it."""

    message_id: int
    reply: str
    mode: str
    topic: str
    difficulty: str
    comfort_signal: str
    concepts: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    difficulty_changed: bool = False
    topic_changed: bool = False
    tokens_used: int = 0
    question_solved: bool = False
    difficulty_increased: bool = False
    problem_id: Optional[int] = None
    # "bank" | "generated" | "improvised" | None. "improvised" means no real problem
    # was available and the model was asked to make one up, which is the degraded
    # path and is labelled so a caller can tell.
    problem_origin: Optional[str] = None
