"""Static verification of generated assessment items. Nothing here asks a model:
an item is kept only if running code proves it.

An MCQ is proven by the code in its own stem when that code prints something, and
otherwise by a short `verify_code` that must compute the answer rather than quote it."""

import ast
import re
from dataclasses import dataclass

from app.core.exceptions import ExecutorUnavailable
from app.core.text import normalize_output
from app.core.topics import MISCONCEPTIONS, TOPICS
from app.models.code_eval import Language
from app.services.assessment.sanitize import reveals_bug
from app.services.execution.base import ExecStatus, ExecutionProvider
from app.services.execution.judge import judge
from app.services.execution.run_code import run_code

DIFFICULTIES = ("easy", "medium", "hard")
DEBUG_LANGUAGES = {"python": Language.PYTHON, "cpp": Language.CPP}
MAX_VERIFY_LINES = 2
_STEM_CODE = re.compile(r"```(?:python|py)?[^\n]*\n(.*?)```", re.DOTALL)


@dataclass(frozen=True)
class Check:
    ok: bool
    reason: str | None = None


def _fail(reason: str) -> Check:
    return Check(False, reason)


def _code_lines(code: str) -> int:
    return sum(1 for line in (code or "").splitlines() if line.strip())


def verify_mcq(item: dict, provider: ExecutionProvider | None = None) -> Check:
    if item.get("topic") not in TOPICS:
        return _fail("unknown topic")
    if item.get("difficulty") not in DIFFICULTIES:
        return _fail("unknown difficulty")
    options = item.get("options") or []
    if not 3 <= len(options) <= 5:
        return _fail("needs 3-5 options")
    answer = item.get("answer_index")
    if not isinstance(answer, int) or not 0 <= answer < len(options):
        return _fail("answer_index out of range")

    texts = [normalize_output(str(o.get("text", ""))) for o in options]
    if any(not t for t in texts) or len(set(texts)) != len(texts):
        return _fail("options must be non-empty and distinct")
    if options[answer].get("misconception"):
        return _fail("the correct option carries a misconception tag")
    for i, option in enumerate(options):
        tag = option.get("misconception")
        if i != answer and tag is not None and tag not in MISCONCEPTIONS:
            return _fail(f"unknown misconception tag {tag!r}")

    try:
        stem_code = _STEM_CODE.search(item.get("stem") or "")
        if stem_code:
            printed = _run_python(stem_code.group(1), provider)
            if printed is None:
                return _fail("stem code did not run cleanly")
            if printed:
                if printed != texts[answer]:
                    return _fail(f"stem code printed {printed!r}, key says {texts[answer]!r}")
                return Check(True)

        code = item.get("verify_code") or ""
        if not code.strip() or _code_lines(code) > MAX_VERIFY_LINES:
            return _fail(f"verify_code must be 1-{MAX_VERIFY_LINES} lines")
        if _hardcodes(code, texts[answer]):
            return _fail("verify_code hardcodes the answer")
        printed = _run_python(code, provider)
    except ExecutorUnavailable:
        return _fail("executor unavailable")
    if printed is None:
        return _fail("verify_code did not run cleanly")
    if printed != texts[answer]:
        return _fail(f"verify_code printed {printed!r}, key says {texts[answer]!r}")
    return Check(True)


def _hardcodes(code: str, answer: str) -> bool:
    """A literal in the code that already spells the answer proves nothing."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    return any(isinstance(node, ast.Constant) and str(node.value) == answer
               for node in ast.walk(tree))


def _run_python(code: str, provider) -> str | None:
    report = run_code(Language.PYTHON, code, [("", None)], provider=provider)
    outcome = report.outcomes[0]
    if not report.compiled or outcome.status is not ExecStatus.OK:
        return None
    return normalize_output(outcome.actual_stdout)


def verify_debug(item: dict, test_cases, provider: ExecutionProvider | None = None) -> Check:
    if item.get("topic") not in TOPICS:
        return _fail("unknown topic")
    if item.get("difficulty") not in DIFFICULTIES:
        return _fail("unknown difficulty")
    if item.get("bug_type") not in MISCONCEPTIONS:
        return _fail("unknown bug_type")
    language = DEBUG_LANGUAGES.get(item.get("language"))
    if language is None:
        return _fail("language must be python or cpp")
    fixed, buggy = item.get("fixed_code") or "", item.get("buggy_code") or ""
    if not fixed.strip() or not buggy.strip():
        return _fail("missing code")
    if normalize_output(fixed) == normalize_output(buggy):
        return _fail("buggy code is identical to the fix")
    if reveals_bug(buggy, fixed, item["language"]):
        return _fail("buggy code has a comment that gives the bug away")
    cases = list(test_cases)
    if not cases:
        return _fail("problem has no tests")

    try:
        good = judge(language, fixed, cases, provider)
        bad = judge(language, buggy, cases, provider)
    except ExecutorUnavailable:
        return _fail("executor unavailable")
    if not good.all_passed:
        return _fail(f"fixed code does not pass ({good.split.passed}/{good.split.total})")
    if not bad.compiled:
        return _fail("buggy code does not compile")
    if bad.all_passed:
        return _fail("buggy code passes every test")
    return Check(True)
