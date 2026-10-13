"""Chat-facing hint paths: level override, approach hints, and ladder isolation."""

from app.models.code_eval import Language
from app.models.learning import HintEvent, LearningEvent
from app.services.hints.prompts import APPROACH_TEMPLATES
from app.services.hints.service import (
    approach_hint,
    highest_level,
    next_level,
    request_hint,
)
from tests.conftest import FakeExecutionProvider, ok
from tests.services.hints import test_hints as base
from tests.services.hints.test_hints import SOLUTION, FakeHintLLM, attempt

user = base.user
problem = base.problem


def test_level_override_skips_the_ladder(session, user, problem):
    attempt(session, user, problem, "3\n0\n")
    llm = FakeHintLLM("Which value should the running maximum start from?")

    hint = request_hint(session, user.id, problem.id, level=3, runnable=llm)

    assert (hint.level, hint.source) == (3, "llm")
    assert "LEVEL 3" in llm.prompts[0]


def test_approach_hint_needs_no_submission_and_logs_as_chat(session, user, problem):
    llm = FakeHintLLM("What should your program print for a single number?")

    hint = approach_hint(session, user.id, problem.id, level=1,
                         language=Language.C, runnable=llm)

    assert (hint.level, hint.source, hint.evaluation_id) == (1, "llm", None)
    assert "APPROACH LEVEL 1" in llm.prompts[0]
    assert "Print the largest value." in llm.prompts[0]
    assert "has not written any code" in llm.prompts[0]
    event = session.query(HintEvent).one()
    assert (event.source, event.evaluation_id, event.level) == ("chat", None, 1)


def test_approach_hint_blocks_a_full_solution_twice_then_uses_the_template(
        session, user, problem):
    llm = FakeHintLLM(f"```python\n{SOLUTION}\n```")

    hint = approach_hint(session, user.id, problem.id, level=3, language=Language.PYTHON,
                         runnable=llm, provider=FakeExecutionProvider([ok("3\n-4\n")]))

    assert len(llm.prompts) == 2
    assert (hint.source, hint.text, hint.was_blocked) == ("template", APPROACH_TEMPLATES[3], True)
    assert session.query(HintEvent).one().was_blocked is True


def test_chat_hints_move_neither_the_practice_ladder_nor_mastery(session, user, problem):
    attempt(session, user, problem, "3\n0\n")
    llm = FakeHintLLM("Think about negative numbers.")

    request_hint(session, user.id, problem.id, level=4, source="chat", runnable=llm)
    approach_hint(session, user.id, problem.id, level=4, language=Language.C, has_code=True,
                  runnable=llm)

    assert "print(0)" in llm.prompts[-1] and "has not written" not in llm.prompts[-1]
    assert next_level(session, user.id, problem.id) == 2
    assert highest_level(session, user.id, problem.id) == 4
    attempt(session, user, problem, "3\n0\n")
    latest = session.query(LearningEvent).order_by(LearningEvent.id.desc()).first()
    assert latest.hint_level_used == 1
    assert request_hint(session, user.id, problem.id, runnable=llm).level == 2
