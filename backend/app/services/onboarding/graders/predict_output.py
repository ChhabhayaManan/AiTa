"""Predict-output: the student's text against the stored output, whitespace-tolerant."""

from app.core.text import normalize_output
from app.models.onboarding import DiagnosticItem
from app.services.execution.base import ExecutionProvider
from app.services.onboarding.graders.sandbox import is_blank
from app.services.onboarding.types import Grade


def grade(item: DiagnosticItem, answer: dict, provider: ExecutionProvider | None = None) -> Grade:
    expected = item.key["expected_output"]
    text = answer.get("text")
    score = 0.0 if is_blank(text) else float(normalize_output(text) == normalize_output(expected))
    why = ("Your output matches what the program prints." if score
           else "The program prints this; compare it with yours line by line.")
    return Grade(score, "key", {"correct": score >= 0.5, "expected": expected, "why": why})
