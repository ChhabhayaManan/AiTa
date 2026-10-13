"""Importing every model module here keeps SQLAlchemy's mapper registry complete.

Without it, an entry point that imports only one model (a script, a worker) fails at
mapper configuration time on relationships that name a class it never loaded.
"""

from app.models import (  # noqa: F401
    book,
    chat,
    code_eval,
    content_player,
    feedback,
    learning,
    llm_call,
    problem,
    recommendation,
    user,
)
