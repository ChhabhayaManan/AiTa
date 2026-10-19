"""One grade function per code item kind, all with the same interface."""

from collections.abc import Callable

from app.models.onboarding import DiagnosticItem
from app.services.execution.base import ExecutionProvider
from app.services.onboarding.graders import fill_blank, find_bug, predict_output, write_code
from app.services.onboarding.types import Grade

GRADERS: dict[str, Callable[[DiagnosticItem, dict, ExecutionProvider | None], Grade]] = {
    "predict_output": predict_output.grade,
    "find_bug": find_bug.grade,
    "fill_blank": fill_blank.grade,
    "write_code": write_code.grade,
}
