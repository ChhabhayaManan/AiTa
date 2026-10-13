"""Chunked open-licence programming books, embedded for the chatbot's search_books tool."""

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, Column, Integer, String, Text, UniqueConstraint
from sqlalchemy.types import TypeDecorator

from app.core.database import Base

EMBED_DIM = 384


class EmbeddingVector(TypeDecorator):
    """pgvector on Postgres; JSON elsewhere so the sqlite test schema still builds."""

    impl = JSON
    cache_ok = True
    comparator_factory = Vector.comparator_factory

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(Vector(EMBED_DIM))
        return dialect.type_descriptor(JSON())


class BookChunk(Base):
    __tablename__ = "book_chunks"
    __table_args__ = (
        UniqueConstraint("source_id", "position", name="uq_book_chunks_source_position"),
    )

    id           = Column(Integer, primary_key=True, index=True)
    source_id    = Column(String(64), nullable=False, index=True)
    source_title = Column(String(255), nullable=False)
    license      = Column(String(64), nullable=False)
    url          = Column(String(500), nullable=True)
    chapter      = Column(String(255), nullable=False, default="")
    section      = Column(String(255), nullable=False, default="")
    lang_tag     = Column(String(10), nullable=False, index=True)
    position     = Column(Integer, nullable=False)
    text         = Column(Text, nullable=False)
    tokens       = Column(Integer, nullable=False, default=0)
    embedding    = Column(EmbeddingVector(), nullable=True)
