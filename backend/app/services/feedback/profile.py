from datetime import datetime, timezone
from typing import Dict

from sqlalchemy.orm import Session

from app.models.user import LearningProfile


def update_profile(db: Session, user_id: int, patterns: Dict, narrative: Dict) -> Dict:
    """Write the run's signals back onto the learner's profile and commit.

    Returns only the fields that actually changed; that dict is what the report
    persists as `profile_updates`.
    """
    p = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()
    if not p:
        return {}
    updates = {}

    new_weak = list(dict.fromkeys(
        (p.weak_areas or []) + patterns["weak_concepts"] + narrative.get("next_topics", [])[:2]
    ))[:10]
    if set(new_weak) != set(p.weak_areas or []):
        p.weak_areas = new_weak
        updates["weak_areas"] = new_weak

    new_err = list(dict.fromkeys(
        (p.error_patterns or []) + [e[:60] for e in patterns["errors"][:3]]
    ))[:15]
    if set(new_err) != set(p.error_patterns or []):
        p.error_patterns = new_err
        updates["error_patterns"] = new_err

    cm = narrative.get("concept_map", {})
    if cm:
        cur = dict(p.topic_scores or {})
        for topic, score in cm.items():
            cur[topic] = round((cur.get(topic, score) * 0.7 + score * 0.3), 3)
        p.topic_scores = cur
        updates["topic_scores"] = cur

    if narrative.get("next_topics"):
        p.recommended_next = narrative["next_topics"][:5]
        updates["recommended_next"] = p.recommended_next

    p.last_updated_by_agent = datetime.now(timezone.utc)
    db.commit()
    return updates
