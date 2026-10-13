"""Chatbot threads and their messages; a message's tool calls and citations ride along as JSON."""

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.sql import func

from app.core.database import Base


class ChatThread(Base):
    __tablename__ = "chat_threads"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                        nullable=False, index=True)
    mode       = Column(String(10), nullable=False, default="aita", server_default="aita")
    title      = Column(String(120), nullable=True)
    summary    = Column(Text, nullable=True)
    # How many of the thread's oldest messages `summary` stands for.
    summary_upto = Column(Integer, nullable=False, default=0, server_default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    __table_args__ = (
        Index("ix_chat_messages_thread_created", "thread_id", "created_at"),
    )

    id              = Column(Integer, primary_key=True, index=True)
    thread_id       = Column(Integer, ForeignKey("chat_threads.id", ondelete="CASCADE"),
                             nullable=False, index=True)
    user_id         = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                             nullable=False, index=True)
    role            = Column(String(16), nullable=False)
    content         = Column(Text, nullable=False)
    tool_calls      = Column(JSON, nullable=True)
    citations       = Column(JSON, nullable=True)
    moderation_flag = Column(String(16), nullable=True)
    thumbs          = Column(String(4), nullable=True)
    model           = Column(String(120), nullable=True)
    tokens          = Column(Integer, nullable=True)
    latency_ms      = Column(Integer, nullable=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
