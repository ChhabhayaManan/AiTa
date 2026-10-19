from collections import Counter

from sqlalchemy.orm import Session

from app.models.learning import DebugChallenge, McqQuestion
from app.models.problem import Problem
from app.services.assessment.sanitize import strip_bug_annotations
from app.services.assessment.verify import verify_debug, verify_mcq

_MCQ_FIELDS = ("topic", "difficulty", "language", "stem", "options", "answer_index",
               "verify_code", "explanations")
_DEBUG_FIELDS = ("topic", "difficulty", "language", "statement", "buggy_code", "fixed_code",
                 "bug_type")


def _upsert(db: Session, model, external_id: str, values: dict) -> bool:
    row = db.query(model).filter(model.external_id == external_id).first()
    created = row is None
    if created:
        row = model(external_id=external_id)
        db.add(row)
    for key, value in values.items():
        setattr(row, key, value)
    return created


def seed(db: Session, bank: dict, provider=None) -> Counter:
    """Every item is re-verified before it is written, so a hand-edited bank cannot
    seed an item whose answer key or bug is no longer proven by execution."""
    report: Counter = Counter()

    for item in bank.get("mcqs", []) + bank.get("diagnostic", []):
        check = verify_mcq(item, provider)
        if not check.ok:
            report["mcq rejected"] += 1
            continue
        values = {k: item.get(k) for k in _MCQ_FIELDS}
        values["language"] = values["language"] or "python"
        values["verify_code"] = values["verify_code"] or ""
        values["explanations"] = values["explanations"] or []
        values["is_diagnostic"] = bool(item.get("is_diagnostic"))
        values["reviewed"] = True
        report["mcq created" if _upsert(db, McqQuestion, item["external_id"], values)
               else "mcq updated"] += 1

    for item in bank.get("debug", []):
        item = {**item, "buggy_code": strip_bug_annotations(
            item.get("buggy_code") or "", item.get("fixed_code") or "", item.get("language"))}
        problem = (db.query(Problem)
                   .filter(Problem.external_id == item.get("problem_external_id")).first())
        if problem is None:
            report["debug rejected: problem not seeded"] += 1
            continue
        check = verify_debug(item, problem.test_cases, provider)
        if not check.ok:
            report["debug rejected"] += 1
            continue
        values = {k: item.get(k) for k in _DEBUG_FIELDS}
        values["problem_id"] = problem.id
        values["reviewed"] = True
        report["debug created" if _upsert(db, DebugChallenge, item["external_id"], values)
               else "debug updated"] += 1

    db.commit()
    return report
