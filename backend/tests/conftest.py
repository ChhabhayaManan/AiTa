import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models import (  # noqa: F401  -- registers every table on Base.metadata
    code_eval, content_player, feedback, problem, recommendation, user,
)
from app.services.execution.base import (
    ExecLimits, ExecResult, ExecStatus, ExecutionProvider,
)


@pytest.fixture
def session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with sessionmaker(bind=engine)() as db:
        yield db


class FakeExecutionProvider(ExecutionProvider):
    def __init__(self, results: list[ExecResult]):
        self.results = results
        self.calls: list[dict] = []

    def run_batch(self, language, source, stdins, limits):
        self.calls.append({"language": language, "source": source, "stdins": list(stdins)})
        return self.results[: len(stdins)]


def ok(stdout: str, time_ms: int = 5) -> ExecResult:
    return ExecResult(status=ExecStatus.OK, stdout=stdout, time_ms=time_ms)


def failing(status: ExecStatus, stderr: str = "",
            compile_output: str | None = None) -> ExecResult:
    return ExecResult(status=status, stderr=stderr, compile_output=compile_output)


@pytest.fixture
def limits():
    return ExecLimits()
