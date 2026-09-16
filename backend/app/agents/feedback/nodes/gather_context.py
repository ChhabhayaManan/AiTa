from typing import Dict, Optional

from sqlalchemy.orm import Session

from app.agents.feedback.state import FeedbackState
from app.models.code_eval import CodeEvaluation, CodeSubmission
from app.models.content_player import ContentPlayerSession
from app.models.feedback import FeedbackType
from app.models.user import LearningProfile, User


def _user_context(db: Session, user_id: int) -> Dict:
    u = db.query(User).filter(User.id == user_id).first()
    p = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()
    return {
        "username": u.username if u else "student",
        "skill": u.skill_level.value if u and u.skill_level else "beginner",
        "languages": u.preferred_languages or [],
        "goals": u.learning_goals or [],
        "weak_areas": p.weak_areas or [] if p else [],
        "error_patterns": p.error_patterns or [] if p else [],
        "accuracy": p.accuracy_rate or 0.0 if p else 0.0,
    }


def _eval_context(db: Session, eval_id: int) -> Optional[Dict]:
    ev = db.query(CodeEvaluation).filter(CodeEvaluation.id == eval_id).first()
    if not ev:
        return None
    sub = db.query(CodeSubmission).filter(CodeSubmission.id == ev.submission_id).first()
    return {
        "language": sub.language.value if sub else "unknown",
        "code": (sub.code or "")[:1500] if sub else "",
        "overall": ev.overall_score,
        "correctness": ev.correctness_score,
        "complexity": ev.complexity_score,
        "efficiency": ev.efficiency_score,
        "style": ev.style_score,
        "verification": ev.verification_status,
        "tests_passed": ev.tests_passed,
        "tests_total": ev.tests_total,
        "issues": ev.issues or [],
        "time_complexity": ev.time_complexity,
        "key_improvements": ev.key_improvements or [],
        "learning_points": ev.learning_points or [],
        "best_practices": ev.best_practices_used or [],
        "anti_patterns": ev.anti_patterns or [],
        "summary": ev.summary or "",
    }


def _cp_context(db: Session, session_id: int) -> Optional[Dict]:
    s = (db.query(ContentPlayerSession)
         .filter(ContentPlayerSession.id == session_id).first())
    if not s:
        return None
    return {
        "topic": s.topic or "",
        "mode": s.mode if isinstance(s.mode, str) else s.mode.value if s.mode else "qa",
        "concepts": s.concepts_covered or [],
        "mastery": s.mastery_signals or [],
        "weak": s.weak_signals or [],
        "confusion": s.confusion_detected,
        "messages": s.total_messages,
    }


def gather_context(state: FeedbackState) -> FeedbackState:
    state.log("Collecting context from upstream agents.")
    state.user_ctx = _user_context(state.db, state.user_id)
    state.eval_ctx = (_eval_context(state.db, state.evaluation_id)
                      if state.evaluation_id else None)
    state.cp_ctx = (_cp_context(state.db, state.cp_session_id)
                    if state.cp_session_id else None)

    if not state.eval_ctx and not state.cp_ctx:
        raise ValueError("Provide at least one of evaluation_id or cp_session_id.")

    state.feedback_type = (
        FeedbackType.COMBINED if state.eval_ctx and state.cp_ctx else
        FeedbackType.CODE_REVIEW if state.eval_ctx else
        FeedbackType.LEARNING_RECAP
    )
    state.log(f"Type: {state.feedback_type.value} | Tone: {state.tone.value}")
    return state
