import json
import pathlib

from app.agents.code_eval.schemas import GeneratedCase, GeneratedTests
from app.models.problem import Problem
from app.services.execution.base import ExecResult, ExecStatus
from scripts.ingest_problems import DATA, ingest
from tests.conftest import FakeExecutionProvider

ROWS = [
    {"external_id": "dsa-a", "source": "dsa",
     "statement": "Read n on the first line and print n.",
     "constraints": "", "topic": "io", "difficulty": "easy"},
    {"external_id": "dsa-b", "source": "dsa",
     "statement": "Read n on the first line and print n plus one.",
     "constraints": "", "topic": "io", "difficulty": "easy"},
]


def generated():
    return GeneratedTests(
        reference_solution="print(input())",
        cases=[GeneratedCase(kind="normal", stdin=f"{i}\n", expected_stdout=str(i),
                             rationale="r") for i in (1, 2, 3)],
    )


def ok_provider():
    return FakeExecutionProvider([
        ExecResult(status=ExecStatus.OK, stdout="1\n"),
        ExecResult(status=ExecStatus.OK, stdout="2\n"),
        ExecResult(status=ExecStatus.OK, stdout="3\n"),
    ])


def test_creates_problems_and_cases(session):
    report = ingest(session, ROWS, generator=lambda **k: generated(),
                    provider=ok_provider(), pause=0)
    assert report.created == 2
    assert report.generated == 2
    assert session.query(Problem).count() == 2


def test_rerun_is_idempotent(session):
    ingest(session, ROWS, generator=lambda **k: generated(),
           provider=ok_provider(), pause=0)

    def explode(**kwargs):
        raise AssertionError("must not call the generator on a rerun")

    report = ingest(session, ROWS, generator=explode, provider=ok_provider(), pause=0)
    assert report.created == 0
    assert report.skipped == 2
    assert session.query(Problem).count() == 2


def test_limit_stops_early(session):
    report = ingest(session, ROWS, generator=lambda **k: generated(),
                    provider=ok_provider(), limit=1, pause=0)
    assert report.seen == 1
    assert session.query(Problem).count() == 1


def test_unverified_problems_are_reported_not_fatal(session):
    bad = FakeExecutionProvider([
        ExecResult(status=ExecStatus.OK, stdout="9\n"),
        ExecResult(status=ExecStatus.OK, stdout="9\n"),
        ExecResult(status=ExecStatus.OK, stdout="9\n"),
    ])
    report = ingest(session, ROWS[:1], generator=lambda **k: generated(),
                    provider=bad, pause=0)
    assert report.unverified == ["dsa-a"]
    assert report.generated == 0


def test_shipped_bank_is_valid():
    rows = json.loads(pathlib.Path(DATA).read_text(encoding="utf-8"))
    assert len(rows) == 25
    assert len({r["external_id"] for r in rows}) == 25
    for row in rows:
        assert row["source"] in ("mbpp", "dsa")
        assert row["difficulty"] in ("easy", "medium", "hard")
        lowered = row["statement"].lower()
        assert "print" in lowered, row["external_id"]
        assert "line" in lowered, row["external_id"]


def test_shipped_bank_ingests_without_network(session):
    rows = json.loads(pathlib.Path(DATA).read_text(encoding="utf-8"))
    report = ingest(session, rows, generator=lambda **k: generated(),
                    provider=ok_provider(), pause=0)
    assert report.created == 25
    assert report.generated == 25
    assert session.query(Problem).count() == 25
