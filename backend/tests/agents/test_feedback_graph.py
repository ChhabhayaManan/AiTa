"""Whole-pipeline tests for the Feedback Agent. Offline — a fake runnable stands in
for the LLM, so the graph runs with no network and no live database."""

import pytest

from app.agents.feedback.graph import generate_feedback
from app.agents.feedback.nodes.persist import HEADLINE_LIMIT
from app.agents.feedback.schemas import FeedbackNarrative
from app.models.code_eval import CodeEvaluation, CodeSubmission, Language
from app.models.content_player import ContentPlayerSession
from app.models.feedback import FeedbackReport, FeedbackTone, FeedbackType
from app.models.user import LearningProfile, User


@pytest.fixture
def user(session):
    u = User(email="s@example.com", username="student", hashed_password="x")
    session.add(u)
    session.commit()
    session.add(LearningProfile(user_id=u.id, weak_areas=["loops"],
                                error_patterns=[], topic_scores={}))
    session.commit()
    return u


def make_evaluation(session, user, **overrides):
    submission = CodeSubmission(user_id=user.id, language=Language.PYTHON,
                                code="print(1)", title="t")
    session.add(submission)
    session.commit()
    fields = dict(
        submission_id=submission.id, user_id=user.id, overall_score=55.0,
        correctness_score=50.0, complexity_score=40.0, efficiency_score=70.0,
        style_score=80.0, verification_status="verified", tests_passed=1,
        tests_total=2, status="done",
        issues=[{"severity": "error", "category": "logic", "message": "off by one"}],
        best_practices_used=["clear names"], learning_points=["boundaries"],
        anti_patterns=[], summary="Nearly there.",
    )
    fields.update(overrides)
    evaluation = CodeEvaluation(**fields)
    session.add(evaluation)
    session.commit()
    return evaluation


def make_cp_session(session, user, **overrides):
    fields = dict(
        user_id=user.id, mode="qa", topic="recursion", total_messages=6,
        concepts_covered=["base case"], mastery_signals=["tracing"],
        weak_signals=["recursion depth"], confusion_detected=True,
    )
    fields.update(overrides)
    cp = ContentPlayerSession(**fields)
    session.add(cp)
    session.commit()
    return cp


def narrative():
    return FeedbackNarrative(
        headline="Solid attempt with one boundary bug",
        summary="You got the shape of the solution right.",
        strengths=["clear names"],
        errors=["off by one at the last index"],
        misconceptions=["ranges are inclusive"],
        action_items=["Trace the loop on a 1-element input"],
        concept_map={"loops": 0.5, "indexing": 0.4},
        next_topics=["indexing", "loop invariants"],
        motivational="You are one small fix away.",
    )


class ProviderError(Exception):
    """Stands in for whatever the provider SDK raises.

    A real caller never raises a pre-wrapped `LLMUnavailable` — `invoke_with_retry`
    is what wraps it. The message deliberately contains no rate-limit marker from
    `app.core.llm._RATE_LIMIT_MARKERS`, so the retry budget is not spent sleeping.
    """


class FakeSynthesiseRunnable:
    """Mirrors what `structured(..., include_raw=True)` hands back."""

    _UNSET = object()

    def __init__(self, result=_UNSET, error=None, tokens=321):
        self.result = narrative() if result is self._UNSET else result
        self.error = error
        self.tokens = tokens
        self.payloads = []

    def invoke(self, payload):
        self.payloads.append(payload)
        if self.error:
            raise self.error
        return {"parsed": self.result, "raw": _Raw(self.tokens)}


class _Raw:
    def __init__(self, tokens):
        self.usage_metadata = {"total_tokens": tokens}


def unavailable():
    """The failure path, entered the way production enters it: the provider raises
    and `invoke_with_retry` turns that into `LLMUnavailable`."""
    return FakeSynthesiseRunnable(error=ProviderError("upstream call failed"))


def test_happy_path_persists_the_narrative(session, user):
    evaluation = make_evaluation(session, user)
    runnable = FakeSynthesiseRunnable()

    report = generate_feedback(
        session, user.id, evaluation.id, None, FeedbackTone.ENCOURAGING,
        synthesise_runnable=runnable,
    )

    assert report.pattern_only is False
    assert report.headline == "Solid attempt with one boundary bug"
    assert report.summary == "You got the shape of the solution right."
    assert report.strengths == ["clear names"]
    assert report.errors == ["off by one at the last index"]
    assert report.misconceptions == ["ranges are inclusive"]
    assert report.action_items == ["Trace the loop on a 1-element input"]
    assert report.concept_map == {"loops": 0.5, "indexing": 0.4}
    assert report.next_topics == ["indexing", "loop invariants"]
    assert report.motivational == "You are one small fix away."
    assert report.tokens_used == 321
    assert report.agent_steps
    assert len(runnable.payloads) == 1


def test_llm_unavailable_is_labelled_not_hidden(session, user):
    evaluation = make_evaluation(session, user)

    report = generate_feedback(
        session, user.id, evaluation.id, None, FeedbackTone.ENCOURAGING,
        synthesise_runnable=unavailable(),
    )

    assert report.pattern_only is True
    assert report.tokens_used == 0
    assert report.misconceptions == []
    # The headline must tell the student this is not the detailed analysis.
    assert "could not be generated" in report.headline
    assert "fallback" not in report.headline.lower()
    # The pattern findings still reach the student.
    assert report.errors == ["[logic] off by one"]
    assert report.strengths == ["clear names"]
    assert "correctness" in report.next_topics
    assert report.concept_map == {"correctness": 0.3, "complexity": 0.3}
    assert report.action_items
    # The provider's own error text must not reach a step the student reads.
    assert not any("upstream call failed" in s for s in report.agent_steps)


def test_an_unparseable_narrative_is_labelled_like_an_outage(session, user):
    """`invoke_with_retry` returns parsed=None rather than raising when structured
    output fails to parse. That must be labelled, not persisted as empty prose."""
    evaluation = make_evaluation(session, user)

    report = generate_feedback(
        session, user.id, evaluation.id, None, FeedbackTone.ENCOURAGING,
        synthesise_runnable=FakeSynthesiseRunnable(result=None),
    )

    assert report.pattern_only is True
    assert report.misconceptions == []
    assert "could not be generated" in report.headline
    assert "fallback" not in report.headline.lower()
    assert report.errors == ["[logic] off by one"]
    assert report.strengths == ["clear names"]
    assert report.concept_map == {"correctness": 0.3, "complexity": 0.3}
    assert report.action_items


def test_profile_is_updated_on_the_happy_path(session, user):
    evaluation = make_evaluation(session, user)
    generate_feedback(session, user.id, evaluation.id, None,
                      FeedbackTone.CONSTRUCTIVE,
                      synthesise_runnable=FakeSynthesiseRunnable())

    profile = session.query(LearningProfile).filter(
        LearningProfile.user_id == user.id).one()
    assert set(profile.weak_areas) >= {"loops", "correctness", "complexity",
                                       "indexing"}
    assert profile.error_patterns == ["[logic] off by one"]
    assert profile.topic_scores == {"loops": 0.5, "indexing": 0.4}
    assert profile.recommended_next == ["indexing", "loop invariants"]
    assert profile.last_updated_by_agent is not None


def test_profile_is_updated_on_the_failure_path(session, user):
    evaluation = make_evaluation(session, user)
    report = generate_feedback(
        session, user.id, evaluation.id, None, FeedbackTone.CONSTRUCTIVE,
        synthesise_runnable=unavailable(),
    )

    profile = session.query(LearningProfile).filter(
        LearningProfile.user_id == user.id).one()
    assert set(profile.weak_areas) >= {"loops", "correctness", "complexity"}
    assert profile.error_patterns == ["[logic] off by one"]
    assert profile.topic_scores == {"correctness": 0.3, "complexity": 0.3}
    assert report.profile_updates["recommended_next"] == ["correctness", "complexity"]


def test_feedback_type_is_code_review_from_an_evaluation(session, user):
    evaluation = make_evaluation(session, user)
    report = generate_feedback(session, user.id, evaluation.id, None,
                               FeedbackTone.ENCOURAGING,
                               synthesise_runnable=FakeSynthesiseRunnable())
    assert report.feedback_type == FeedbackType.CODE_REVIEW


def test_feedback_type_is_learning_recap_from_a_session(session, user):
    cp = make_cp_session(session, user)
    report = generate_feedback(session, user.id, None, cp.id,
                               FeedbackTone.ENCOURAGING,
                               synthesise_runnable=FakeSynthesiseRunnable())
    assert report.feedback_type == FeedbackType.LEARNING_RECAP


def test_feedback_type_is_combined_from_both(session, user):
    evaluation = make_evaluation(session, user)
    cp = make_cp_session(session, user)
    report = generate_feedback(session, user.id, evaluation.id, cp.id,
                               FeedbackTone.CHALLENGING,
                               synthesise_runnable=FakeSynthesiseRunnable())
    assert report.feedback_type == FeedbackType.COMBINED
    assert report.tone == FeedbackTone.CHALLENGING


def test_session_signals_reach_the_pattern_analysis(session, user):
    cp = make_cp_session(session, user)
    report = generate_feedback(
        session, user.id, None, cp.id, FeedbackTone.ENCOURAGING,
        synthesise_runnable=unavailable(),
    )

    assert report.errors == ["Confusion on topic: 'recursion'"]
    assert report.strengths == ["tracing"]
    assert report.next_topics == ["recursion depth"]


def test_an_overlong_headline_is_clamped_not_raised(session, user):
    """`headline` is the only bounded column in the row, and the profile write has
    already committed by the time it is inserted. SQLite does not enforce VARCHAR
    length, so this asserts the clamp rather than the DataError it prevents."""
    evaluation = make_evaluation(session, user)
    verbose = narrative()
    verbose.headline = "y" * 500

    report = generate_feedback(
        session, user.id, evaluation.id, None, FeedbackTone.ENCOURAGING,
        synthesise_runnable=FakeSynthesiseRunnable(result=verbose),
    )

    limit = FeedbackReport.__table__.columns["headline"].type.length
    assert limit == HEADLINE_LIMIT, "the clamp must match the column it protects"
    assert len(report.headline) == HEADLINE_LIMIT
    assert report.headline.endswith("…")


def test_a_headline_at_the_limit_is_untouched(session, user):
    evaluation = make_evaluation(session, user)
    exact = narrative()
    exact.headline = "y" * HEADLINE_LIMIT

    report = generate_feedback(
        session, user.id, evaluation.id, None, FeedbackTone.ENCOURAGING,
        synthesise_runnable=FakeSynthesiseRunnable(result=exact),
    )

    assert report.headline == "y" * HEADLINE_LIMIT


def test_neither_id_supplied_raises_value_error(session, user):
    with pytest.raises(ValueError):
        generate_feedback(session, user.id, None, None, FeedbackTone.ENCOURAGING,
                          synthesise_runnable=FakeSynthesiseRunnable())


def test_unknown_ids_raise_value_error(session, user):
    with pytest.raises(ValueError):
        generate_feedback(session, user.id, 9999, 9999, FeedbackTone.ENCOURAGING,
                          synthesise_runnable=FakeSynthesiseRunnable())
