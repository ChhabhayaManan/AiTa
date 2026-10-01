"""The Profiling Agent's steps. The only code allowed to write learning_events,
topic_mastery, and the mirrored fields of LearningProfile."""

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.topics import PREREQUISITES, TOPIC_LABELS, TOPICS, clean_misconceptions, normalise_topic
from app.models.learning import LearningEvent, TopicMastery
from app.models.user import LearningProfile
from app.services.profiling.mastery import (
    PRIOR,
    WEAK_BELOW,
    WEIGHTS,
    band,
    confidence,
    updated_mastery,
)

MISCONCEPTION_WINDOW = 30
HINT_WINDOW = 10
RECENT_EVENTS = 10


@dataclass
class EventInput:
    user_id: int
    kind: str
    score: float
    raw_topic: str | None
    item_id: int | None = None
    hint_level: int = 0
    misconceptions: list[str] = field(default_factory=list)
    source_ref: str | None = None


def record_event(db: Session, event_in: EventInput) -> LearningEvent:
    if event_in.kind not in WEIGHTS:
        raise ValueError(f"unknown event kind: {event_in.kind}")
    event = LearningEvent(
        user_id=event_in.user_id,
        kind=event_in.kind,
        item_id=event_in.item_id,
        topic=normalise_topic(event_in.raw_topic),
        raw_topic=(event_in.raw_topic or None) and event_in.raw_topic[:100],
        score=max(0.0, min(1.0, event_in.score)),
        weight=WEIGHTS[event_in.kind],
        hint_level_used=event_in.hint_level,
        misconceptions=clean_misconceptions(event_in.misconceptions),
        source_ref=event_in.source_ref,
    )
    db.add(event)
    db.flush()
    return event


def update_mastery(db: Session, event: LearningEvent) -> TopicMastery | None:
    if event.topic is None:
        return None
    row = db.get(TopicMastery, (event.user_id, event.topic))
    if row is None:
        row = TopicMastery(user_id=event.user_id, topic=event.topic,
                           mastery=PRIOR, evidence_count=0)
        db.add(row)
    event.mastery_before = row.mastery
    row.mastery = updated_mastery(row.mastery, event.weight, event.score)
    row.evidence_count += 1
    row.last_event_at = datetime.now(timezone.utc)
    event.mastery_after = row.mastery
    db.flush()
    return row


def _mastery_rows(db: Session, user_id: int) -> dict[str, TopicMastery]:
    rows = db.query(TopicMastery).filter(TopicMastery.user_id == user_id).all()
    return {r.topic: r for r in rows}


def derive_profile(db: Session, user_id: int) -> LearningProfile:
    """Mirror topic_mastery into LearningProfile so existing readers keep working. This
    is the only writer of every field it sets."""
    rows = _mastery_rows(db, user_id)
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()
    if profile is None:
        profile = LearningProfile(user_id=user_id)
        db.add(profile)

    profile.topic_scores = {t: round(r.mastery, 3) for t, r in rows.items()}
    profile.weak_areas = [t for t, r in rows.items()
                          if band(r.mastery, r.evidence_count) == "weak"]
    profile.strong_areas = [t for t, r in rows.items()
                            if band(r.mastery, r.evidence_count) == "mastered"]

    def value(topic: str) -> float:
        return rows[topic].mastery if topic in rows else PRIOR

    open_topics = [t for t in TOPICS
                   if all(value(p) >= WEAK_BELOW for p in PREREQUISITES[t])
                   and band(value(t), rows[t].evidence_count if t in rows else 0) != "mastered"]
    profile.recommended_next = sorted(open_topics, key=value)[:3]
    profile.error_patterns = [tag for tag, _ in top_misconceptions(db, user_id)[:5]]

    scores = [s for (s,) in db.query(LearningEvent.score)
              .filter(LearningEvent.user_id == user_id).all()]
    profile.accuracy_rate = round(sum(scores) / len(scores), 3) if scores else 0.0
    profile.last_updated_by_agent = datetime.now(timezone.utc)
    db.flush()
    return profile


def _recent_events(db: Session, user_id: int, limit: int, kinds=None) -> list[LearningEvent]:
    query = db.query(LearningEvent).filter(LearningEvent.user_id == user_id)
    if kinds:
        query = query.filter(LearningEvent.kind.in_(kinds))
    return query.order_by(LearningEvent.id.desc()).limit(limit).all()


def top_misconceptions(db: Session, user_id: int) -> list[tuple[str, int]]:
    counts = Counter()
    for event in _recent_events(db, user_id, MISCONCEPTION_WINDOW):
        counts.update(event.misconceptions or [])
    return counts.most_common()


def hint_reliance(db: Session, user_id: int) -> float:
    events = _recent_events(db, user_id, HINT_WINDOW, kinds=("code", "debug"))
    if not events:
        return 0.0
    return round(sum(e.hint_level_used for e in events) / len(events), 2)


def mastery_snapshot(db: Session, user_id: int) -> dict:
    rows = _mastery_rows(db, user_id)

    def value(topic: str) -> float:
        return rows[topic].mastery if topic in rows else PRIOR

    topics = []
    for topic in TOPICS:
        row = rows.get(topic)
        count = row.evidence_count if row else 0
        mastery = value(topic)
        topics.append({
            "topic": topic,
            "label": TOPIC_LABELS[topic],
            "mastery": round(mastery, 3),
            "evidence_count": count,
            "confidence": round(confidence(count), 2),
            "band": band(mastery, count),
            "last_event_at": row.last_event_at if row else None,
            "prerequisites": list(PREREQUISITES[topic]),
            "unlocked": all(value(p) >= WEAK_BELOW for p in PREREQUISITES[topic]),
        })

    return {
        "topics": topics,
        "top_misconceptions": [
            {"tag": tag, "count": count} for tag, count in top_misconceptions(db, user_id)
        ],
        "hint_reliance": hint_reliance(db, user_id),
        "recent_events": _recent_events(db, user_id, RECENT_EVENTS),
    }
