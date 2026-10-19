from typing import Dict, Optional

from sqlalchemy.orm import Session

from app.agents.feedback.state import FeedbackState
from app.core.topics import TOPIC_LABELS, normalise_topic
from app.models.code_eval import CodeEvaluation, CodeSubmission
from app.models.content_player import ContentPlayerSession
from app.models.feedback import FeedbackType
from app.models.learning import LearningEvent, TopicMastery
from app.models.problem import ExecRole, ExecutionResult, Problem
from app.models.user import LearningProfile, User
from app.services.hints.service import failing_case, highest_level, reference_sources
from app.services.personalisation import style_line
from app.services.profiling.mastery import SEED_KINDS
from app.services.profiling.service import top_misconceptions


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
        "style": style_line(db, user_id),
    }


def _learning_context(db: Session, user_id: int, ev: CodeEvaluation, sub) -> Dict:
    """What the learner model knows around this attempt. Read-only: the Feedback Agent
    never writes the profile."""
    problem = db.get(Problem, sub.problem_id) if sub and sub.problem_id else None
    topic = normalise_topic(problem.topic) if problem else None
    mastery = db.get(TopicMastery, (user_id, topic)) if topic else None
    case = failing_case(db, ev)
    statuses = [r.status for r in db.query(ExecutionResult)
                .filter(ExecutionResult.evaluation_id == ev.id,
                        ExecutionResult.role == ExecRole.STUDENT)
                .order_by(ExecutionResult.id)]
    recent = (db.query(LearningEvent)
              .filter(LearningEvent.user_id == user_id, LearningEvent.kind.notin_(SEED_KINDS))
              .order_by(LearningEvent.id.desc()).limit(5).all())
    return {
        "problem_id": problem.id if problem else None,
        "topic": topic,
        "topic_label": TOPIC_LABELS.get(topic, topic) if topic else None,
        "mastery": round(mastery.mastery, 2) if mastery else None,
        "evidence": mastery.evidence_count if mastery else 0,
        "failing_case": case.__dict__ if case else None,
        "case_statuses": statuses,
        "misconception_counts": dict(top_misconceptions(db, user_id)),
        "this_attempt_misconceptions": next(
            (e.misconceptions or [] for e in db.query(LearningEvent).filter(
                LearningEvent.source_ref == f"evaluation:{ev.id}",
                LearningEvent.kind.notin_(SEED_KINDS))), []),
        "hint_level": (highest_level(db, user_id, problem.id) if problem else 0),
        "recent_events": [
            {"kind": e.kind, "topic": e.topic, "score": round(e.score, 2),
             "misconceptions": e.misconceptions or []}
            for e in recent
        ],
        "references": reference_sources(problem),
        "test_cases": list(problem.test_cases) if problem else [],
    }


def _eval_context(db: Session, eval_id: int) -> Optional[Dict]:
    ev = db.query(CodeEvaluation).filter(CodeEvaluation.id == eval_id).first()
    if not ev:
        return None
    sub = db.query(CodeSubmission).filter(CodeSubmission.id == ev.submission_id).first()
    return {
        "learning": _learning_context(db, ev.user_id, ev, sub),
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
    learning = state.eval_ctx["learning"] if state.eval_ctx else None
    if learning and learning["problem_id"]:
        level = learning["hint_level"]
        state.log(f"Hint ladder on this problem: L{level} of 4 used since the last pass."
                  if level else "No hints used on this problem since the last pass.")
    return state
