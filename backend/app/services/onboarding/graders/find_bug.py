"""Find-bug: half for the right line, half for a fix that passes the tests."""

from app.models.onboarding import DiagnosticItem
from app.services.execution.base import ExecutionProvider
from app.services.onboarding.graders.sandbox import (
    GRADED_BY,
    is_blank,
    outcome_line,
    run_tests,
    skipped,
)
from app.services.onboarding.types import Grade


def grade(item: DiagnosticItem, answer: dict, provider: ExecutionProvider | None = None) -> Grade:
    bug_line = item.key["bug_line"]
    fixed_code = item.key["fixed_code"]
    line_ok = answer.get("line") == bug_line
    fix_code = answer.get("fix_code")

    fix_ok, fix_why = False, "No fix was submitted."
    if not is_blank(fix_code):
        judgement = run_tests(item, fix_code, provider)
        if judgement is None:
            return skipped(fixed_code, bug_line=bug_line)
        fix_ok, fix_why = judgement.all_passed, outcome_line(judgement)

    score = 0.5 * line_ok + 0.5 * fix_ok
    line_why = "Right line." if line_ok else f"The bug is on line {bug_line}."
    return Grade(score, GRADED_BY, {"correct": score >= 0.5, "expected": fixed_code,
                                    "bug_line": bug_line, "why": f"{line_why} {fix_why}"})
