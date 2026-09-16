"""Whole-turn tests for the Content Player chat graph. Offline — a fake runnable
stands in for the tutor model, so the graph runs with no network and no live
database."""

import pytest

from app.agents.code_eval.schemas import GeneratedCase, GeneratedTests
from app.agents.content_player.graph import run_chat_turn
from app.agents.content_player.schemas import TutorReply
from app.core.exceptions import LLMUnavailable, SessionNotFound
from app.models.content_player import ContentPlayerMessage, ContentPlayerSession
from app.models.problem import (
    Difficulty,
    IOMode,
    Problem,
    ProblemSource,
    TestCase,
    TestCaseKind,
    TestCaseOrigin,
)
from app.models.user import LearningProfile, User
from app.services.problems.listing import list_bank_problems
from app.services.problems.schemas import ProblemDraft
from tests.conftest import FakeExecutionProvider, ok

SOLVED_MESSAGE = "def solve():\n    pass\n\naccuracy: 90%"
WRONG_MESSAGE = "def solve():\n    pass\n\naccuracy: 20%"

LATENCY_MS = 137


class FakeClock:
    """`invoke_with_retry` reads the wall clock, so a fake that answers instantly
    reports a latency of 0 — and `latency_ms` defaults to 0 in the column too, which
    leaves no value that proves the wiring exists. Driving the clock from the fake
    gives the call a latency of its own, the way `tokens_used` already has one.

    Replaces the whole module reference rather than patching `time.monotonic`
    globally, so only `app.core.llm` sees it. `sleep` advances instead of waiting.
    """

    def __init__(self):
        self.now = 0.0

    def reset(self):
        self.now = 0.0

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.now += seconds

    def advance_ms(self, milliseconds: int) -> None:
        self.now += milliseconds / 1000


_clock = FakeClock()


@pytest.fixture(autouse=True)
def clock(monkeypatch):
    _clock.reset()
    monkeypatch.setattr("app.core.llm.time", _clock)
    return _clock


@pytest.fixture
def user(session):
    u = User(email="s@example.com", username="student", hashed_password="x")
    session.add(u)
    session.commit()
    session.add(LearningProfile(user_id=u.id, weak_areas=[], error_patterns=[],
                                topic_scores={}, recommended_next=[]))
    session.commit()
    return u


def make_session(db, user, **overrides):
    fields = dict(user_id=user.id, mode="qa", topic="recursion", language="python",
                  difficulty="medium", concepts_covered=["base case"],
                  mastery_signals=[], weak_signals=[], solved_questions=[],
                  consecutive_easy_solves=0, total_messages=0, total_tokens_used=0)
    fields.update(overrides)
    cp = ContentPlayerSession(**fields)
    db.add(cp)
    db.commit()
    return cp


def seed_problem(db, external_id, statement_hash, topic="arrays",
                 difficulty=Difficulty.EASY):
    problem = Problem(
        source=ProblemSource.DSA, external_id=external_id,
        statement=f"Statement for {external_id}.", statement_hash=statement_hash,
        topic=topic, difficulty=difficulty, io_mode=IOMode.STDIN_STDOUT,
    )
    db.add(problem)
    db.commit()
    db.add(TestCase(
        problem_id=problem.id, kind=TestCaseKind.SAMPLE, stdin="1 2\n",
        expected_stdout="3", stdin_hash=statement_hash[:63] + "c",
        origin=TestCaseOrigin.CROSS_CHECKED, ordinal=1,
    ))
    db.commit()
    return problem


def seed_bank(db):
    return [
        seed_problem(db, "dsa-first", "a" * 64),
        seed_problem(db, "dsa-second", "b" * 64),
        seed_problem(db, "dsa-third", "c" * 64),
        seed_problem(db, "dsa-fourth", "d" * 64, difficulty=Difficulty.MEDIUM),
    ]


def reply(**overrides):
    fields = dict(reply="Let's trace the base case together.",
                  concepts=["recursion", "base case"], mastery=["tracing"],
                  weak=["call stack"], suggestions=["What ends the recursion?"])
    fields.update(overrides)
    return TutorReply(**fields)


class _Raw:
    def __init__(self, tokens):
        self.usage_metadata = {"total_tokens": tokens}


class ProviderError(Exception):
    """Stands in for whatever the provider SDK raises.

    A real caller never raises a pre-wrapped `LLMUnavailable` — `invoke_with_retry`
    is what wraps it. The message deliberately contains no rate-limit marker from
    `app.core.llm._RATE_LIMIT_MARKERS`, so the retry budget is not spent sleeping.
    """


class FakeRespondRunnable:
    """Mirrors what `structured(..., include_raw=True)` hands back."""

    _UNSET = object()

    def __init__(self, result=_UNSET, error=None, tokens=140, latency_ms=LATENCY_MS):
        self.result = reply() if result is self._UNSET else result
        self.error = error
        self.tokens = tokens
        self.latency_ms = latency_ms
        self.payloads = []

    def invoke(self, payload):
        self.payloads.append(payload)
        _clock.advance_ms(self.latency_ms)
        if self.error:
            raise self.error
        return {"parsed": self.result, "raw": _Raw(self.tokens)}


def unavailable():
    return FakeRespondRunnable(error=ProviderError("upstream call failed"))


def messages_of(db, cp):
    return (db.query(ContentPlayerMessage)
            .filter(ContentPlayerMessage.session_id == cp.id)
            .order_by(ContentPlayerMessage.id).all())


def forbid_generation(monkeypatch):
    """For turns that must be answered out of the bank: generation is not merely
    unnecessary, it must not run at all."""
    def explode(*args, **kwargs):
        raise AssertionError("generation must not run on a bank hit")

    monkeypatch.setattr("app.services.problems.generation.generate_problem", explode)


def unavailable_generation(monkeypatch):
    """The bank misses and nothing can be generated — the degraded branch."""
    def unavailable_(*args, **kwargs):
        raise LLMUnavailable("no problem could be written")

    monkeypatch.setattr("app.services.problems.generation.generate_problem",
                        unavailable_)


def fake_generation(monkeypatch, provider):
    """The generation path with both of its model calls faked, as
    tests/api/test_content_player_api.py does it."""
    draft = ProblemDraft(
        title="Sum Two Integers",
        statement="Read two integers on one line and print their sum.",
        constraints=["1 <= a <= 100"],
        hints=["Splitting a line"],
    )

    class FakeDraft:
        def invoke(self, prompt):
            return {"parsed": draft, "raw": None}

    monkeypatch.setattr("app.services.problems.generation.get_chat_model",
                        lambda **kwargs: None)
    monkeypatch.setattr("app.services.problems.generation.structured",
                        lambda model, schema: FakeDraft())
    monkeypatch.setattr(
        "app.services.test_generation.generate_tests._default_generator",
        lambda **kwargs: GeneratedTests(
            reference_solution="print(sum(map(int, input().split())))",
            cases=[GeneratedCase(kind="normal", stdin=s, expected_stdout=e,
                                 rationale="r")
                   for s, e in (("1 2\n", "3"), ("4 5\n", "9"), ("0 0\n", "0"))],
        ),
    )
    monkeypatch.setattr("app.services.execution.run_code.get_provider",
                        lambda: provider)


def test_a_full_turn_persists_the_reply_and_its_signals(session, user):
    cp = make_session(session, user)
    runnable = FakeRespondRunnable()

    turn = run_chat_turn(session, cp.id, user.id, "How does a base case end things?",
                         respond_runnable=runnable)

    rows = messages_of(session, cp)
    assert [r.role for r in rows] == ["user", "assistant"]
    assert rows[0].content == "How does a base case end things?"
    assert rows[1].content == "Let's trace the base case together."
    assert rows[1].id == turn.message_id
    # The usage the call reported, on the row it describes.
    assert rows[1].tokens_used == 140
    assert rows[1].model_used
    assert rows[1].latency_ms == LATENCY_MS

    session.refresh(cp)
    assert cp.total_messages == 2
    assert cp.total_tokens_used == 140
    assert set(cp.concepts_covered) == {"base case", "recursion"}
    assert cp.mastery_signals == ["tracing"]
    assert cp.weak_signals == ["call stack"]
    assert cp.last_message_at is not None
    # The model that answered, not the decommissioned one the column used to name.
    assert cp.agent_model and "llama-3.3-70b-versatile" not in cp.agent_model

    assert turn.reply == "Let's trace the base case together."
    assert turn.suggestions == ["What ends the recursion?"]
    assert turn.tokens_used == 140
    assert turn.problem_id is None
    assert len(runnable.payloads) == 1


def test_the_sentinel_protocol_is_gone_from_the_prompt(session, user):
    cp = make_session(session, user)
    runnable = FakeRespondRunnable()

    run_chat_turn(session, cp.id, user.id, "How does a base case end things?",
                  respond_runnable=runnable)

    system = runnable.payloads[0][0][1]
    assert "AGENT_META" not in system
    assert "END_META" not in system


def test_a_second_turn_accumulates_rather_than_replacing(session, user):
    cp = make_session(session, user)
    run_chat_turn(session, cp.id, user.id, "First question about base cases?",
                  respond_runnable=FakeRespondRunnable())
    run_chat_turn(session, cp.id, user.id, "Second question about base cases?",
                  respond_runnable=FakeRespondRunnable(
                      result=reply(concepts=["induction"], mastery=[], weak=[])))

    session.refresh(cp)
    assert cp.total_messages == 4
    assert cp.total_tokens_used == 280
    assert set(cp.concepts_covered) == {"base case", "recursion", "induction"}


def test_llm_unavailable_keeps_the_student_turn_and_writes_no_reply(session, user):
    cp = make_session(session, user)

    with pytest.raises(LLMUnavailable) as excinfo:
        run_chat_turn(session, cp.id, user.id, "How does a base case end things?",
                      respond_runnable=unavailable())

    assert "try again" in excinfo.value.detail
    # The provider's own error text must not reach the student.
    assert "upstream call failed" not in excinfo.value.detail

    rows = messages_of(session, cp)
    assert [r.role for r in rows] == ["user"]
    assert rows[0].content == "How does a base case end things?"

    session.refresh(cp)
    assert cp.total_messages == 1
    assert cp.total_tokens_used == 0
    assert cp.agent_model is None
    assert cp.concepts_covered == ["base case"]
    assert cp.last_message_at is not None


def test_a_failed_turn_applies_none_of_the_students_signals(session, user,
                                                            monkeypatch):
    """The 503 tells the student to try again, so this turn's signals must not be
    counted now and then again off the message they resend."""
    forbid_generation(monkeypatch)
    seed_bank(session)
    cp = make_session(session, user, topic="arrays", difficulty="easy")

    with pytest.raises(LLMUnavailable):
        run_chat_turn(session, cp.id, user.id, SOLVED_MESSAGE,
                      respond_runnable=unavailable())

    session.refresh(cp)
    assert cp.consecutive_easy_solves == 0
    assert cp.difficulty == "easy"
    assert cp.solved_questions == []
    assert cp.confusion_detected is False

    # The retry is the turn that counts, and it counts once.
    run_chat_turn(session, cp.id, user.id, SOLVED_MESSAGE,
                  respond_runnable=FakeRespondRunnable())

    session.refresh(cp)
    assert cp.consecutive_easy_solves == 1
    assert cp.total_messages == 3
    assert [r.role for r in messages_of(session, cp)] == ["user", "user", "assistant"]


def test_a_failed_turn_does_not_move_the_topic_or_flag_confusion(session, user,
                                                                 monkeypatch):
    cp = make_session(session, user, topic="arrays", difficulty="hard")
    message = ("I am completely lost, can you explain again how binary tree "
               "traversal reaches every leaf from the root?")

    with pytest.raises(LLMUnavailable):
        run_chat_turn(session, cp.id, user.id, message,
                      respond_runnable=unavailable())

    session.refresh(cp)
    assert cp.topic == "arrays"
    assert cp.difficulty == "hard"
    # Confusion and the difficulty drop come from the same signal, so they move
    # together: neither is applied until a turn completes.
    assert cp.confusion_detected is False
    session.refresh(user)
    assert not user.interested_topics


def test_an_unparseable_reply_is_treated_exactly_like_an_outage(session, user):
    """`invoke_with_retry` returns parsed=None rather than raising when structured
    output fails to parse. With nothing to say, that is the same situation."""
    cp = make_session(session, user)

    with pytest.raises(LLMUnavailable):
        run_chat_turn(session, cp.id, user.id, "How does a base case end things?",
                      respond_runnable=FakeRespondRunnable(result=None))

    assert [r.role for r in messages_of(session, cp)] == ["user"]
    session.refresh(cp)
    assert cp.total_messages == 1


def test_a_bank_problem_is_served_and_never_served_twice(session, user, monkeypatch):
    forbid_generation(monkeypatch)
    first, second, *_ = seed_bank(session)
    cp = make_session(session, user, mode="walkthrough", topic="arrays",
                      difficulty="easy")

    opening = run_chat_turn(session, cp.id, user.id, "Teach me how arrays work.",
                            respond_runnable=FakeRespondRunnable())

    assert opening.problem_origin == "bank"
    assert opening.problem_id == first.id
    session.refresh(cp)
    assert cp.solved_questions == [first.id]

    runnable = FakeRespondRunnable()
    solved = run_chat_turn(session, cp.id, user.id, SOLVED_MESSAGE,
                           respond_runnable=runnable)

    assert solved.question_solved is True
    assert solved.problem_origin == "bank"
    assert solved.problem_id == second.id
    session.refresh(cp)
    assert cp.solved_questions == [first.id, second.id]
    # The statement is in the prompt, so the tutor sets that problem rather than
    # inventing one.
    assert "Statement for dsa-second." in runnable.payloads[0][0][1]


def test_a_bank_miss_generates_a_problem_that_is_not_in_the_bank(session,
                                                                 monkeypatch):
    u = User(email="g@example.com", username="gen", hashed_password="x")
    session.add(u)
    session.commit()
    seed_problem(session, "dsa-arrays-only", "e" * 64, topic="arrays")
    cp = make_session(session, u, mode="walkthrough", topic="graphs",
                      difficulty="medium")
    fake_generation(monkeypatch,
                    FakeExecutionProvider([ok("3\n"), ok("9\n"), ok("0\n")]))

    turn = run_chat_turn(session, cp.id, u.id, "Teach me how graphs work.",
                         respond_runnable=FakeRespondRunnable())

    assert turn.problem_origin == "generated"
    stored = session.query(Problem).filter(Problem.id == turn.problem_id).one()
    assert stored.source is ProblemSource.GENERATED
    assert len(stored.test_cases) == 3
    assert turn.problem_id not in [p.id for p in list_bank_problems(session)]

    session.refresh(cp)
    assert cp.solved_questions == [turn.problem_id]


def test_a_legacy_question_key_does_not_strand_the_session(session, user,
                                                           monkeypatch):
    """Sessions that ran before this migration hold `_question_key` strings in
    `solved_questions`. They name no problem, so they are dropped — and they must not
    fail state validation, which would report a live session as a missing one.

    "²" is a digit to `str.isdigit` but not a number to `int`, so it has to be
    screened out by the same step rather than reaching the conversion."""
    forbid_generation(monkeypatch)
    first, *_ = seed_bank(session)
    cp = make_session(session, user, topic="arrays", difficulty="easy",
                      solved_questions=["arrays_easy", "²", 7])

    turn = run_chat_turn(session, cp.id, user.id, SOLVED_MESSAGE,
                         respond_runnable=FakeRespondRunnable())

    assert turn.problem_id == first.id
    session.refresh(cp)
    # The legacy string is gone and the real id it never was is not invented.
    assert cp.solved_questions == [7, first.id]


def test_no_problem_available_falls_back_to_an_improvised_one(session, user,
                                                              monkeypatch):
    """The degraded branch: the bank misses, nothing can be generated, so the tutor
    is asked for a problem in prose the way it always used to be — and the turn says
    so."""
    unavailable_generation(monkeypatch)
    cp = make_session(session, user, mode="walkthrough", topic="graphs",
                      difficulty="easy")
    runnable = FakeRespondRunnable()

    turn = run_chat_turn(session, cp.id, user.id, "Teach me how graphs work.",
                         respond_runnable=runnable)

    assert turn.problem_origin == "improvised"
    assert turn.problem_id is None
    system = runnable.payloads[0][0][1]
    assert "No curated problem was available" in system
    assert "LeetCode EASY level problem about graphs" in system

    session.refresh(cp)
    # Nothing was set, so nothing is excluded next time.
    assert cp.solved_questions == []


def test_three_solves_bump_the_difficulty_and_reset_the_streak(session, user,
                                                               monkeypatch):
    forbid_generation(monkeypatch)
    seed_bank(session)
    cp = make_session(session, user, topic="arrays", difficulty="easy")

    for _ in range(2):
        turn = run_chat_turn(session, cp.id, user.id, SOLVED_MESSAGE,
                             respond_runnable=FakeRespondRunnable())
        assert turn.difficulty_increased is False
        assert turn.difficulty == "easy"

    session.refresh(cp)
    assert cp.consecutive_easy_solves == 2

    third = run_chat_turn(session, cp.id, user.id, SOLVED_MESSAGE,
                          respond_runnable=FakeRespondRunnable())

    assert third.difficulty_increased is True
    assert third.difficulty == "medium"
    assert third.difficulty_changed is True
    session.refresh(cp)
    assert cp.difficulty == "medium"
    assert cp.consecutive_easy_solves == 0


def test_a_wrong_submission_resets_the_streak(session, user, monkeypatch):
    forbid_generation(monkeypatch)
    seed_bank(session)
    cp = make_session(session, user, topic="arrays", difficulty="easy")

    for _ in range(2):
        run_chat_turn(session, cp.id, user.id, SOLVED_MESSAGE,
                      respond_runnable=FakeRespondRunnable())
    session.refresh(cp)
    assert cp.consecutive_easy_solves == 2

    turn = run_chat_turn(session, cp.id, user.id, WRONG_MESSAGE,
                         respond_runnable=FakeRespondRunnable())

    assert turn.question_solved is False
    assert turn.problem_id is None
    session.refresh(cp)
    assert cp.consecutive_easy_solves == 0
    assert cp.difficulty == "easy"


def test_a_short_message_does_not_switch_the_topic(session, user):
    cp = make_session(session, user, topic="arrays")

    turn = run_chat_turn(session, cp.id, user.id,
                         "binary tree traversal from the root",
                         respond_runnable=FakeRespondRunnable())

    assert turn.topic_changed is False
    assert turn.topic == "arrays"
    session.refresh(cp)
    assert cp.topic == "arrays"


def test_a_long_message_about_another_topic_switches_everything(session, user):
    cp = make_session(session, user, topic="arrays")
    message = ("Can you explain how binary tree traversal works, starting from "
               "the root node and walking down to every leaf?")

    turn = run_chat_turn(session, cp.id, user.id, message,
                         respond_runnable=FakeRespondRunnable())

    assert turn.topic_changed is True
    assert turn.topic == "trees"
    session.refresh(cp)
    assert cp.topic == "trees"
    session.refresh(user)
    assert "trees" in user.interested_topics
    profile = session.query(LearningProfile).filter(
        LearningProfile.user_id == user.id).one()
    assert "trees" in profile.recommended_next


def test_confusion_is_read_from_the_student_not_asserted_by_the_model(session, user):
    cp = make_session(session, user)

    turn = run_chat_turn(session, cp.id, user.id,
                         "I don't understand any of this, I am stuck.",
                         respond_runnable=FakeRespondRunnable())

    assert turn.comfort_signal == "struggling"
    session.refresh(cp)
    assert cp.confusion_detected is True
    # Struggling drops one level from the session's medium.
    assert cp.difficulty == "easy"


def test_an_unknown_session_raises(session, user):
    with pytest.raises(SessionNotFound):
        run_chat_turn(session, 9999, user.id, "Hello?",
                      respond_runnable=FakeRespondRunnable())


def test_another_users_session_raises(session, user):
    other = User(email="o@example.com", username="other", hashed_password="x")
    session.add(other)
    session.commit()
    cp = make_session(session, other)

    with pytest.raises(SessionNotFound):
        run_chat_turn(session, cp.id, user.id, "Hello?",
                      respond_runnable=FakeRespondRunnable())

    assert messages_of(session, cp) == []


def test_an_empty_message_raises(session, user):
    cp = make_session(session, user)

    with pytest.raises(ValueError):
        run_chat_turn(session, cp.id, user.id, "   ",
                      respond_runnable=FakeRespondRunnable())

    assert messages_of(session, cp) == []
