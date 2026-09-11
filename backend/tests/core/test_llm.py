import pytest

from app.core.exceptions import LLMUnavailable
from app.core.llm import LLMUsage, invoke_with_retry


class FakeRunnable:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def invoke(self, payload):
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class FakeRaw:
    def __init__(self, tokens):
        self.usage_metadata = {"total_tokens": tokens}


def ok(value, tokens=42):
    return {"parsed": value, "raw": FakeRaw(tokens)}


def test_returns_parsed_value_and_usage():
    runnable = FakeRunnable([ok("hello", tokens=17)])
    value, usage = invoke_with_retry(runnable, "prompt")
    assert value == "hello"
    assert isinstance(usage, LLMUsage)
    assert usage.tokens == 17
    assert usage.latency_ms >= 0
    assert usage.model


def test_retries_on_rate_limit_then_succeeds():
    runnable = FakeRunnable([Exception("429 Resource has been exhausted"), ok("later")])
    value, _ = invoke_with_retry(runnable, "prompt")
    assert value == "later"
    assert runnable.calls == 2


def test_gives_up_after_attempts_and_raises_domain_error():
    runnable = FakeRunnable([Exception("429 quota exceeded")] * 3)
    with pytest.raises(LLMUnavailable):
        invoke_with_retry(runnable, "prompt", attempts=2)
    assert runnable.calls == 2


def test_non_rate_limit_error_is_not_retried():
    runnable = FakeRunnable([Exception("invalid schema"), ok("unused")])
    with pytest.raises(LLMUnavailable):
        invoke_with_retry(runnable, "prompt")
    assert runnable.calls == 1


def test_usage_defaults_to_zero_when_raw_has_none():
    runnable = FakeRunnable([{"parsed": "v", "raw": object()}])
    _, usage = invoke_with_retry(runnable, "prompt")
    assert usage.tokens == 0
