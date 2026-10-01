"""The learner model: evidence events, per-topic mastery, and the assessment banks
that feed it. Only the Profiling Agent writes `learning_events` and `topic_mastery`."""

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.sql import func

from app.core.database import Base


class LearningEvent(Base):
    __tablename__ = "learning_events"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                             nullable=False, index=True)
    kind            = Column(String(20), nullable=False)
    item_id         = Column(Integer, nullable=True)
    topic           = Column(String(40), nullable=True, index=True)
    raw_topic       = Column(String(100), nullable=True)
    score           = Column(Float, nullable=False)
    weight          = Column(Float, nullable=False)
    hint_level_used = Column(Integer, nullable=False, default=0)
    misconceptions  = Column(JSON, default=list)
    mastery_before  = Column(Float, nullable=True)
    mastery_after   = Column(Float, nullable=True)
    source_ref      = Column(String(60), nullable=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now(), index=True)


class TopicMastery(Base):
    __tablename__ = "topic_mastery"

    user_id        = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                            primary_key=True)
    topic          = Column(String(40), primary_key=True)
    mastery        = Column(Float, nullable=False)
    evidence_count = Column(Integer, nullable=False, default=0)
    last_event_at  = Column(DateTime(timezone=True), nullable=True)


class HintEvent(Base):
    __tablename__ = "hint_events"

    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                           nullable=False, index=True)
    problem_id    = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"),
                           nullable=False, index=True)
    evaluation_id = Column(Integer, ForeignKey("code_evaluations.id", ondelete="SET NULL"),
                           nullable=True)
    level         = Column(Integer, nullable=False)
    was_blocked   = Column(Boolean, nullable=False, default=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())


class McqQuestion(Base):
    __tablename__ = "mcq_questions"

    id            = Column(Integer, primary_key=True, index=True)
    external_id   = Column(String(60), unique=True, nullable=False)
    topic         = Column(String(40), nullable=False, index=True)
    difficulty    = Column(String(10), nullable=False)
    stem          = Column(Text, nullable=False)
    # [{"text": ..., "misconception": tag | None}, ...]
    options       = Column(JSON, nullable=False)
    answer_index  = Column(Integer, nullable=False)
    # ≤ 2 lines of Python whose output is exactly the correct option's text: the
    # answer key is proven by execution, never by judgement. Never serialised.
    verify_code   = Column(Text, nullable=False)
    explanations  = Column(JSON, default=list)
    is_diagnostic = Column(Boolean, nullable=False, default=False)
    reviewed      = Column(Boolean, nullable=False, default=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())


class McqAttempt(Base):
    __tablename__ = "mcq_attempts"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                          nullable=False, index=True)
    question_id  = Column(Integer, ForeignKey("mcq_questions.id", ondelete="CASCADE"),
                          nullable=False)
    chosen_index = Column(Integer, nullable=False)
    correct      = Column(Boolean, nullable=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())


class DebugChallenge(Base):
    __tablename__ = "debug_challenges"

    id          = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(60), unique=True, nullable=False)
    problem_id  = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"),
                         nullable=False)
    topic       = Column(String(40), nullable=False, index=True)
    difficulty  = Column(String(10), nullable=False)
    language    = Column(String(20), nullable=False)
    statement   = Column(Text, nullable=False)
    buggy_code  = Column(Text, nullable=False)
    # Kept only to re-verify the challenge; never serialised to a client.
    fixed_code  = Column(Text, nullable=False)
    bug_type    = Column(String(40), nullable=False)
    reviewed    = Column(Boolean, nullable=False, default=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())


class DebugAttempt(Base):
    __tablename__ = "debug_attempts"

    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                            nullable=False, index=True)
    challenge_id   = Column(Integer, ForeignKey("debug_challenges.id", ondelete="CASCADE"),
                            nullable=False)
    submitted_code = Column(Text, nullable=False)
    tests_passed   = Column(Integer, nullable=False, default=0)
    tests_total    = Column(Integer, nullable=False, default=0)
    fixed          = Column(Boolean, nullable=False, default=False)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())
