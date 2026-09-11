from typing import Optional

from pydantic import BaseModel


class ProblemSummary(BaseModel):
    """One row in the problem picker."""
    id:          int
    title:       str
    statement:   str            # already carries the multi-test preamble
    source:      str
    topic:       Optional[str] = None
    difficulty:  Optional[str] = None
    constraints: Optional[str] = None
    test_count:  int = 0
    # One worked example, so a student can see the exact shape of stdin and stdout.
    sample_input:  Optional[str] = None
    sample_output: Optional[str] = None
