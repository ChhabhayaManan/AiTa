r"""One CSV row per onboarding participant for the W1 analysis, inside the backend container:

    docker compose -f docker-compose.yml -f docker-compose.local.yml exec backend \
        python -m scripts.export_w1 /tmp/w1.csv
    docker compose -f docker-compose.yml -f docker-compose.local.yml cp \
        backend:/tmp/w1.csv G:/Study/BMP2/docs/study/w1.csv

Read-only. The output path is required and may not be inside the repo."""

import argparse
import csv
from collections import defaultdict
from datetime import timezone
from pathlib import Path
from statistics import median

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.topics import TOPICS
from app.models.onboarding import DiagnosticItem, DiagnosticResponse, OnboardingRecord
from app.models.user import User
from app.services.onboarding.steps import utc

STEPS = ("welcome", "language", "about", "learning")
PENDING = ("pending", "saved")
COLUMNS = ("user_id", "language", "started_at", "finished_at", "total_s",
           *(f"step_{step}_s" for step in STEPS), "step_diagnostic_s", "drop_off_step",
           "items_asked", "code_items", "theory_items", "skipped_items", "pending_items",
           "item_ms_median", "item_ms_total",
           *(f"seed_{topic}" for topic in TOPICS), "concept_level", "self_rating", "mean_seed",
           "calibration_gap", "title")
# Inside the container the scripts sit at /app/scripts, with no repo around them.
_ROOT = Path(__file__).resolve().parents[2]
REPO = _ROOT if (_ROOT / "backend").is_dir() else None


def _blank(value):
    return "" if value is None else value


def _stamp(moment) -> str:
    return utc(moment).astimezone(timezone.utc).isoformat() if moment else ""


def _seconds(start, end):
    return round((utc(end) - utc(start)).total_seconds(), 1) if start and end else None


def _row(record: OnboardingRecord, language: str, responses: list[DiagnosticResponse]) -> dict:
    durations = record.step_durations or {}
    seeds = {topic: value for topic, (value, _source) in (record.seeds or {}).items()}
    theory = [r for r in responses if r.phase == "theory"]
    mean_seed = round(sum(seeds.values()) / len(seeds), 3) if seeds else None
    gap = (round(record.self_rating / 5 - mean_seed, 3)
           if record.self_rating is not None and mean_seed is not None else None)
    times = [r.ms_taken for r in responses]
    return {
        "user_id": record.user_id,
        "language": language,
        "started_at": _stamp(record.started_at),
        "finished_at": _stamp(record.finished_at),
        "total_s": _blank(_seconds(record.started_at, record.finished_at)),
        **{f"step_{step}_s": _blank(durations.get(step)) for step in STEPS},
        "step_diagnostic_s": _blank(_seconds(record.diagnostic_started_at, record.finished_at)),
        "drop_off_step": "" if record.finished_at else record.current_step,
        "items_asked": len(responses),
        "code_items": len(responses) - len(theory),
        "theory_items": len(theory),
        "skipped_items": sum(r.graded_by == "skipped" for r in responses),
        "pending_items": sum(r.graded_by in PENDING for r in responses),
        "item_ms_median": median(times) if times else "",
        "item_ms_total": sum(times) if times else "",
        **{f"seed_{topic}": _blank(seeds.get(topic)) for topic in TOPICS},
        "concept_level": record.concept_level,
        "self_rating": _blank(record.self_rating),
        "mean_seed": _blank(mean_seed),
        "calibration_gap": _blank(gap),
        "title": _blank(record.title),
    }


def rows(db: Session) -> list[dict]:
    by_user: dict[int, list[DiagnosticResponse]] = defaultdict(list)
    served: dict[int, str] = {}
    responses = (db.query(DiagnosticResponse, DiagnosticItem.language)
                 .join(DiagnosticItem, DiagnosticItem.id == DiagnosticResponse.item_id)
                 .order_by(DiagnosticResponse.order))
    for response, language in responses:
        by_user[response.user_id].append(response)
        if language != "any":
            served.setdefault(response.user_id, language)
    records = (db.query(OnboardingRecord, User.preferred_language)
               .join(User, User.id == OnboardingRecord.user_id)
               .order_by(OnboardingRecord.user_id))
    return [_row(record, served.get(record.user_id, preferred), by_user[record.user_id])
            for record, preferred in records]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("out", help="CSV path, outside the repo")
    out = Path(parser.parse_args(argv).out).resolve()
    if REPO is not None and out.is_relative_to(REPO):
        raise SystemExit(f"Refusing to write {out}: choose a path outside the repo ({REPO}).")
    with SessionLocal() as db:
        exported = rows(db)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(exported)
    print(f"Wrote {len(exported)} rows to {out}")


if __name__ == "__main__":
    main()
