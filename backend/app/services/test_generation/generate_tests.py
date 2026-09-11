import hashlib

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.agents.code_eval.multi_test import merge_cases
from app.agents.code_eval.prompts import REFERENCE_RETRY_PROMPT, TEST_GENERATION_PROMPT
from app.agents.code_eval.schemas import GeneratedTests
from app.core.config import settings
from app.core.llm import get_chat_model, invoke_with_retry, structured
from app.core.text import normalize_output
from app.models.code_eval import Language
from app.models.problem import (
    Problem, ProblemReference, ReferenceStatus, TestCase, TestCaseKind, TestCaseOrigin,
)
from app.services.execution.base import ExecStatus
from app.services.execution.run_code import run_code


class TestSuite(BaseModel):
    problem_id: int
    case_count: int
    reference_solution: str | None
    agreed: int
    dropped: int
    attempts: int
    unverified_reason: str | None


def _default_generator(**kwargs) -> GeneratedTests:
    if kwargs.get("previous"):
        prompt = REFERENCE_RETRY_PROMPT.format(
            statement=kwargs["statement"],
            previous=kwargs["previous"],
            failure=kwargs["failure"],
        )
    else:
        prompt = TEST_GENERATION_PROMPT.format(
            statement=kwargs["statement"],
            constraints=kwargs.get("constraints") or "None stated.",
            count=kwargs["count"],
        )
    runnable = structured(get_chat_model(), GeneratedTests)
    result, _ = invoke_with_retry(runnable, prompt)
    return result


def _stdin_hash(stdin: str) -> str:
    return hashlib.sha256(stdin.encode("utf-8")).hexdigest()


def _cached_suite(problem: Problem) -> TestSuite | None:
    if not problem.test_cases:
        return None
    reference = next(
        (r.source for r in problem.references if r.status is ReferenceStatus.VALIDATED),
        None,
    )
    return TestSuite(
        problem_id=problem.id,
        case_count=len(problem.test_cases),
        reference_solution=reference,
        agreed=len(problem.test_cases),
        dropped=0,
        attempts=0,
        unverified_reason=None,
    )


def generate_tests(db: Session, problem: Problem, *, generator=None,
                   provider=None) -> TestSuite:
    cached = _cached_suite(problem)
    if cached is not None:
        return cached

    generator = generator or _default_generator
    previous = failure = None
    attempts = 0

    while attempts < settings.REFERENCE_MAX_ATTEMPTS:
        attempts += 1
        generated = generator(
            statement=problem.statement,
            constraints=problem.constraints,
            count=settings.TEST_CASES_TARGET,
            previous=previous,
            failure=failure,
        )

        # The reference reads a test count first, so each sub-case is validated by
        # handing it a batch of exactly one. Sub-cases stay independently judged.
        report = run_code(
            Language.PYTHON,
            generated.reference_solution,
            [(merge_cases([case])[0], None) for case in generated.cases],
            provider=provider,
        )

        broken = [o for o in report.outcomes if o.status is not ExecStatus.OK]
        if not report.compiled or len(broken) * 2 > len(report.outcomes):
            previous = generated.reference_solution
            failure = (
                report.compile_output
                or (broken[0].stderr if broken else "reference produced no output")
            )
            continue

        agreed: list[tuple] = []
        dropped = 0
        seen: set[str] = set()
        for case, outcome in zip(generated.cases, report.outcomes):
            if outcome.status is not ExecStatus.OK:
                dropped += 1
                continue
            if normalize_output(outcome.actual_stdout) != normalize_output(case.expected_stdout):
                dropped += 1
                continue
            digest = _stdin_hash(case.stdin)
            if digest in seen:
                continue
            seen.add(digest)
            agreed.append((case, outcome, digest))

        db.add(ProblemReference(
            problem_id=problem.id, language=Language.PYTHON,
            source=generated.reference_solution,
            status=ReferenceStatus.VALIDATED, attempts=attempts,
        ))

        if len(agreed) < settings.TEST_CASES_MIN:
            db.commit()
            db.refresh(problem)
            return TestSuite(
                problem_id=problem.id, case_count=0,
                reference_solution=generated.reference_solution,
                agreed=len(agreed), dropped=dropped, attempts=attempts,
                unverified_reason="insufficient_agreed_tests",
            )

        for ordinal, (case, outcome, digest) in enumerate(agreed, start=1):
            db.add(TestCase(
                problem_id=problem.id,
                kind=TestCaseKind(case.kind),
                stdin=case.stdin,
                expected_stdout=normalize_output(outcome.actual_stdout),
                stdin_hash=digest,
                origin=TestCaseOrigin.CROSS_CHECKED,
                rationale=case.rationale,
                ordinal=ordinal,
            ))
        db.commit()
        db.refresh(problem)

        return TestSuite(
            problem_id=problem.id, case_count=len(agreed),
            reference_solution=generated.reference_solution,
            agreed=len(agreed), dropped=dropped, attempts=attempts,
            unverified_reason=None,
        )

    db.add(ProblemReference(
        problem_id=problem.id, language=Language.PYTHON,
        source=previous or "", status=ReferenceStatus.FAILED, attempts=attempts,
    ))
    db.commit()
    db.refresh(problem)
    return TestSuite(
        problem_id=problem.id, case_count=0, reference_solution=None,
        agreed=0, dropped=0, attempts=attempts,
        unverified_reason="reference_unvalidated",
    )
