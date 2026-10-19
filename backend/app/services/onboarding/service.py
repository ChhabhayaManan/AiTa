"""The onboarding orchestrator: the only module that writes the onboarding tables and
calls the Profiling Agent. The walk, seeding and card it drives are pure."""

from dataclasses import asdict
from datetime import datetime, timezone

from fastapi import BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import InvalidAnswer, OnboardingConflict
from app.core.topics import TOPICS
from app.models.onboarding import DiagnosticItem, DiagnosticResponse, OnboardingRecord
from app.models.user import SkillLevel, User
from app.schemas.onboarding import (
    THEORY_CAP,
    AnswerIn,
    AnswerOut,
    CardOut,
    DiagOut,
    ProfilePatch,
    StateOut,
    TheoryReveal,
)
from app.services.assessment import policy
from app.services.onboarding import bank, pending, profile_card, seeding, steps, walk
from app.services.onboarding.graders import GRADERS
from app.services.onboarding.types import Ask, BankIndex, Resp, Seed
from app.services.profiling.service import record_diagnostic_seed

HOLE_TRIES = 5
# A theory answer inside the block, not yet sent to the judge. Only "pending" rows are
# retried (background, sweep), so the block still goes out in one call.
SAVED = "saved"
_BANDS = {value: band for band, value in seeding.SEED_VALUES.items()}


def now() -> datetime:
    return datetime.now(timezone.utc)


def _record(db: Session, user: User) -> OnboardingRecord:
    record = db.get(OnboardingRecord, user.id)
    if record is None:
        record = OnboardingRecord(user_id=user.id, started_at=now(), step_durations={},
                                  seeds={})
        db.add(record)
        db.commit()
    return record


def _elapsed_s(record: OnboardingRecord) -> float:
    return (now() - steps.utc(record.diagnostic_started_at)).total_seconds()


def _answered_ids(db: Session, user_id: int) -> set[int]:
    return {item_id for (item_id,) in db.query(DiagnosticResponse.item_id)
            .filter(DiagnosticResponse.user_id == user_id)}


def _plan(db: Session, user: User, resps: list[Resp], elapsed_s: float,
          exclude: set[int]) -> tuple[tuple[Ask, DiagnosticItem] | None, BankIndex]:
    """The walk's next ask and a bank item for it. A ref the bank cannot serve is a hole:
    it is dropped from the index and the walk asked again."""
    language = user.preferred_language
    index = bank.bank_index(db, language)
    for _ in range(HOLE_TRIES):
        step = walk.next_step(resps, index, elapsed_s)
        if not isinstance(step, Ask):
            break
        item = bank.fetch(db, step.ref, language, exclude)
        if item is not None:
            return (step, item), index
        index = index - {(step.ref.topic, step.ref.kind, step.ref.difficulty)}
    return None, index


def _phase_of(db: Session, user: User, item: DiagnosticItem, resps: list[Resp],
              exclude: set[int]) -> str:
    """A code item was served before the time cap, so the walk with the clock at zero
    replays the ask it was served for."""
    if item.kind == "theory":
        return "theory"
    found, _ = _plan(db, user, resps, 0.0, exclude)
    if found and found[1].id == item.id:
        return found[0].ref.phase
    return "write" if item.kind == "write_code" else "code"


def topic_map(resps: list[Resp], asking: str | None = None) -> dict[str, str]:
    preview = seeding.seeds(resps)
    code = [r for r in resps if r.ref.phase in walk.CODE_PHASES]
    unscored = {r.ref.topic for r in code} - {r.ref.topic for r in code if r.score is not None}

    def state(topic: str) -> str:
        if topic == asking:
            return "asking"
        if topic in preview:
            seed = preview[topic]
            return "inferred" if seed.source == "inferred" else _BANDS[seed.value]
        return "skipped" if topic in unscored else "unknown"

    return {topic: state(topic) for topic in TOPICS}


def _serve(db: Session, user: User, record: OnboardingRecord) -> DiagOut:
    resps = pending.responses_for(db, user.id)
    if record.finished_at is not None:
        return DiagOut(item=None, order=len(resps), remaining=0, topic_map=topic_map(resps),
                       phase=None, done=True)
    exclude = _answered_ids(db, user.id)
    elapsed = _elapsed_s(record)
    current = record.current_item_id
    if current is not None and current not in exclude:
        item = db.get(DiagnosticItem, current)
        index = bank.bank_index(db, user.preferred_language)
        phase = _phase_of(db, user, item, resps, exclude)
    else:
        found, index = _plan(db, user, resps, elapsed, exclude)
        item, phase = (found[1], found[0].ref.phase) if found else (None, None)
        record.current_item_id = item.id if item else None
        db.commit()
    if item is None:
        return DiagOut(item=None, order=len(resps), remaining=0, topic_map=topic_map(resps),
                       phase=None, done=True)
    left = walk.remaining(resps, index, elapsed)
    return DiagOut(item=bank.payload(item), order=len(resps) + 1, remaining=max(0, left - 1),
                   topic_map=topic_map(resps, item.topic), phase=phase, done=False)


def _walk_done(db: Session, user: User, record: OnboardingRecord) -> bool:
    found, _ = _plan(db, user, pending.responses_for(db, user.id), _elapsed_s(record),
                     _answered_ids(db, user.id))
    return found is None


def next_item(db: Session, user: User) -> DiagOut:
    record = _record(db, user)
    if not steps.background_saved(record):
        raise OnboardingConflict("Finish the background steps before the diagnostic.")
    if record.diagnostic_started_at is None and record.finished_at is None:
        record.diagnostic_started_at = record.language_locked_at = now()
        steps.move_to(record, "diagnostic")
        db.commit()
    return _serve(db, user, record)


def _stored(db: Session, user_id: int, item_id: int) -> DiagnosticResponse | None:
    return (db.query(DiagnosticResponse)
            .filter_by(user_id=user_id, item_id=item_id).one_or_none())


def _theory_reveals(db: Session, user_id: int) -> list[TheoryReveal]:
    rows = (db.query(DiagnosticResponse, DiagnosticItem)
            .join(DiagnosticItem, DiagnosticItem.id == DiagnosticResponse.item_id)
            .filter(DiagnosticResponse.user_id == user_id, DiagnosticResponse.phase == "theory",
                    DiagnosticResponse.graded_by.notin_((pending.PENDING, SAVED)))
            .order_by(DiagnosticResponse.order))
    return [TheoryReveal(item_id=item.id, topic=item.topic, question=item.body["question"],
                         score=resp.score, reveal=resp.reveal, feedback=resp.feedback)
            for resp, item in rows]


def _answer_out(db: Session, user: User, record: OnboardingRecord, row: DiagnosticResponse,
                saved_only: bool, theory: list[TheoryReveal] | None = None) -> AnswerOut:
    following = _serve(db, user, record)
    written = row.phase == "theory"
    return AnswerOut(reveal=None if written else row.reveal,
                     score=None if written else row.score, saved_only=saved_only,
                     theory_reveals=theory or [],
                     topic_map=following.topic_map, next=following)


def _replay(db: Session, user: User, record: OnboardingRecord,
            row: DiagnosticResponse) -> AnswerOut:
    saved_only = row.graded_by == SAVED
    block_sent = row.phase == "theory" and not saved_only
    return _answer_out(db, user, record, row, saved_only,
                       _theory_reveals(db, user.id) if block_sent else None)


def _release(db: Session, user_id: int) -> int:
    """Hand the user's saved theory answers to the judge queue."""
    count = (db.query(DiagnosticResponse)
             .filter(DiagnosticResponse.user_id == user_id, DiagnosticResponse.graded_by == SAVED)
             .update({DiagnosticResponse.graded_by: pending.PENDING}))
    db.commit()
    return count


def _grade_theory_block(db: Session, user_id: int,
                        background_tasks: BackgroundTasks) -> list[TheoryReveal]:
    _release(db, user_id)
    pending.grade_pending_for_user(db, user_id)
    if pending.has_pending(db, user_id):
        background_tasks.add_task(pending.retry_with_backoff, user_id)
    return _theory_reveals(db, user_id)


def answer(db: Session, user: User, data: AnswerIn,
           background_tasks: BackgroundTasks) -> AnswerOut:
    record = _record(db, user)
    stored = _stored(db, user.id, data.item_id)
    if stored is not None:
        return _replay(db, user, record, stored)
    if record.finished_at is not None or data.item_id != record.current_item_id:
        raise OnboardingConflict("That is not the current diagnostic question.")
    item = db.get(DiagnosticItem, data.item_id)
    given = data.answer.model_dump(exclude_none=True)
    if item.kind == "theory" and len(given.get("text") or "") > THEORY_CAP:
        raise InvalidAnswer(f"A theory answer can be at most {THEORY_CAP} characters.")

    resps = pending.responses_for(db, user.id)
    exclude = _answered_ids(db, user.id)
    row = DiagnosticResponse(user_id=user.id, item_id=item.id, order=len(resps) + 1,
                             phase=_phase_of(db, user, item, resps, exclude), answer=given,
                             ms_taken=data.ms_taken)
    if item.kind == "theory":
        row.score, row.graded_by = None, SAVED
    else:
        grade = GRADERS[item.kind](item, given, None)
        row.score, row.graded_by = grade.score, grade.graded_by
        row.reveal, row.feedback = grade.reveal, grade.feedback
    db.add(row)
    record.current_item_id = None
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return _replay(db, user, record, _stored(db, user.id, data.item_id))

    if item.kind != "theory":
        return _answer_out(db, user, record, row, saved_only=False)
    found, _ = _plan(db, user, pending.responses_for(db, user.id), _elapsed_s(record),
                     exclude | {item.id})
    if found is not None:
        return _answer_out(db, user, record, row, saved_only=True)
    graded = _grade_theory_block(db, user.id, background_tasks)
    return _answer_out(db, user, record, row, saved_only=False, theory=graded)


def _card(db: Session, user: User, record: OnboardingRecord) -> CardOut:
    seeds = {topic: Seed(value, source) for topic, (value, source)
             in (record.seeds or {}).items()}
    card = profile_card.build(seeds, record.concept_level, steps.answers(db, user, record),
                              policy.start_topic(db, user.id))
    return CardOut(**asdict(card), theory_pending=pending.has_pending(db, user.id))


def _locked_record(db: Session, user: User) -> OnboardingRecord:
    return (db.query(OnboardingRecord).filter_by(user_id=user.id)
            .populate_existing().with_for_update().one())


def _write_results(db: Session, user: User, record: OnboardingRecord) -> None:
    found = seeding.seeds(pending.responses_for(db, user.id))
    user.skill_level = SkillLevel(seeding.skill_level(found))
    record.seeds = {topic: [seed.value, seed.source] for topic, seed in found.items()}
    record.title = profile_card.title_for(found)
    record.finished_at = now()
    record.current_item_id = None
    steps.move_to(record, "done")
    # Commits the record together with the seeds, which also ends the _locked_record lock.
    record_diagnostic_seed(db, user.id, {topic: seed.value for topic, seed in found.items()})
    db.commit()
    # Picks up theory the sweep graded meanwhile, and recomputes concept level.
    pending.after_regrade(db, user.id)


def finish(db: Session, user: User, background_tasks: BackgroundTasks) -> CardOut:
    record = _record(db, user)
    if record.finished_at is None:
        if record.diagnostic_started_at is None or not _walk_done(db, user, record):
            raise OnboardingConflict("Finish the diagnostic first.")
        # Only never-sent answers are graded here; ones the judge already failed on go to
        # the background retry, so the student never waits on a busy judge twice.
        if _release(db, user.id):
            pending.grade_pending_for_user(db, user.id)
        record = _locked_record(db, user)
        if record.finished_at is None:
            _write_results(db, user, record)
            if pending.has_pending(db, user.id):
                background_tasks.add_task(pending.retry_with_backoff, user.id)
    return _card(db, user, record)


def save_step(db: Session, user: User, step: str, data: BaseModel) -> StateOut:
    record = _record(db, user)
    if step == "language" and record.language_locked_at is not None:
        raise OnboardingConflict("The language is locked once the diagnostic starts.")
    steps.apply(db, user, record, step, data)
    steps.advance(record, step, now())
    db.commit()
    return state(db, user)


def edit_profile(db: Session, user: User, patch: ProfilePatch) -> CardOut:
    record = _record(db, user)
    if record.finished_at is None:
        raise OnboardingConflict("The profile can be edited once onboarding is finished.")
    for step in ("about", "learning"):
        data = getattr(patch, step)
        if data is not None:
            steps.apply(db, user, record, step, data)
    db.commit()
    return _card(db, user, record)


def state(db: Session, user: User) -> StateOut:
    record = _record(db, user)
    diagnostic = card = None
    if record.finished_at is not None:
        card = _card(db, user, record)
    elif record.diagnostic_started_at is not None:
        diagnostic = _serve(db, user, record)
    return StateOut(current_step=record.current_step, answers=steps.answers(db, user, record),
                    diagnostic=diagnostic, card=card)
