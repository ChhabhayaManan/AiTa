from collections import defaultdict
from typing import Dict, List

from sqlalchemy.orm import Session

from app.models.recommendation import Content, Recommendation, UserContentInteraction
from app.models.user import LearningProfile, User
from app.services.recommendations.weights import PREREQUISITES, TOPIC_ADJACENCY


def _extract_user_context(db: Session, user_id: int) -> Dict:
    user    = db.query(User).filter(User.id == user_id).first()
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()

    interactions = db.query(UserContentInteraction).filter(
        UserContentInteraction.user_id == user_id
    ).all()

    seen_ids      = {i.content_id for i in interactions}
    completed_ids = {i.content_id for i in interactions if i.is_completed or i.completion_pct >= 80}
    liked_ids     = {i.content_id for i in interactions if (i.rating or 0) >= 4.0}
    disliked_ids  = {i.content_id for i in interactions if (i.rating or 0) <= 2.0}

    dismissed_ids = {r[0] for r in db.query(Recommendation.content_id).filter(
        Recommendation.user_id == user_id, Recommendation.is_dismissed.is_(True)
    ).all()}

    excluded_ids = completed_ids | dismissed_ids | disliked_ids

    # Time spent per topic — derived from interactions on content
    time_per_topic: Dict[str, float] = defaultdict(float)
    completed_content = db.query(Content).filter(
        Content.id.in_(completed_ids)
    ).all() if completed_ids else []
    for c in completed_content:
        for t in (c.topics or []):
            time_per_topic[t.lower()] += c.duration_mins or 0

    # Parse difficulty preference from learning_goals
    learning_goals = user.learning_goals or [] if user else []
    difficulty_pref = "medium"
    for g in learning_goals:
        if g.startswith("difficulty:"):
            difficulty_pref = g.split(":", 1)[1].strip()
            break

    return {
        "user_id":             user_id,
        "username":            user.username if user else "student",
        "skill_level":         user.skill_level.value if user and user.skill_level else "beginner",
        "difficulty_pref":     difficulty_pref,
        "preferred_languages": [lang.lower() for lang in (user.preferred_languages or [])] if user else [],
        "learning_goals":      [g for g in learning_goals if not g.startswith("difficulty:")],
        "interests":           user.interests or [] if user else [],
        "interested_topics":   (
            user.interested_topics or []
            if user else []
        ) or (user.interests or [] if user else []),
        "weak_areas":          profile.weak_areas if profile else [],
        "strong_areas":        profile.strong_areas if profile else [],
        "topic_scores":        profile.topic_scores if profile else {},
        "error_patterns":      profile.error_patterns if profile else [],
        "preferred_content_types": profile.preferred_content_types if profile else [],
        "accuracy_rate":       profile.accuracy_rate if profile else 0.0,
        "improvement_rate":    profile.improvement_rate if profile else 0.0,
        "time_per_topic":      dict(time_per_topic),
        "seen_content_ids":    seen_ids,
        "completed_ids":       completed_ids,
        "dismissed_ids":       dismissed_ids,
        "excluded_ids":        excluded_ids,
        "liked_ids":           liked_ids,
        "disliked_ids":        disliked_ids,
    }


def _analyse_learning_path(user_ctx: Dict):
    """
    Detects knowledge gaps and determines what to learn next.

    Gap detection:
      - Topics with topic_score < 0.5 (low accuracy)
      - Topics in error_patterns (recurring mistakes)
      - Topics in weak_areas (agent-flagged)

    Next topics:
      - Prerequisites of interested topics not yet started
      - Adjacent topics after completing current ones
    """
    topic_scores  = user_ctx["topic_scores"]
    weak_areas    = {t.lower() for t in user_ctx["weak_areas"]}
    error_topics  = {e.lower() for e in user_ctx["error_patterns"]}
    interested    = [t.lower().replace("_", " ") for t in user_ctx["interested_topics"]]
    time_per_topic = user_ctx["time_per_topic"]

    # Gap topics: low score OR in weak_areas OR in error_patterns
    gap_topics: List[str] = []
    for topic in interested:
        score = topic_scores.get(topic, None)
        if topic in weak_areas or topic in error_topics:
            gap_topics.append(topic)
        elif score is not None and score < 0.5:
            gap_topics.append(topic)

    # Next topics: prerequisites not yet covered + adjacency suggestions
    next_topics: List[str] = []
    for topic in interested:
        prereqs = PREREQUISITES.get(topic, [])
        for p in prereqs:
            if p not in interested and p not in next_topics:
                # Only suggest if user hasn't spent time on it
                if time_per_topic.get(p, 0) < 30:
                    next_topics.append(p)

    # If no gaps and no next, suggest adjacency
    if not next_topics:
        for topic in interested:
            for adj in TOPIC_ADJACENCY.get(topic, []):
                if adj not in interested and adj not in next_topics:
                    next_topics.append(adj)
                    if len(next_topics) >= 3:
                        break

    return gap_topics[:5], next_topics[:5]
