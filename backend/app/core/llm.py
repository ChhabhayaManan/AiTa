import time
from dataclasses import dataclass
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from app.core.config import settings
from app.core.exceptions import LLMUnavailable

_RATE_LIMIT_MARKERS = (
    "429", "resource has been exhausted", "quota", "rate limit",
    "resourceexhausted", "unavailable", "503", "deadline",
)


@dataclass(frozen=True)
class LLMUsage:
    tokens: int
    latency_ms: int
    model: str


def get_chat_model(temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=temperature,
        max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS,
    )


def structured(model: ChatGoogleGenerativeAI, schema: type[BaseModel]):
    return model.with_structured_output(schema, include_raw=True)


def _is_rate_limited(exc: Exception) -> bool:
    text = str(exc).lower()
    return any(marker in text for marker in _RATE_LIMIT_MARKERS)


def _read_usage(raw: Any) -> int:
    metadata = getattr(raw, "usage_metadata", None) or {}
    try:
        return int(metadata.get("total_tokens", 0))
    except (AttributeError, TypeError, ValueError):
        return 0


def invoke_with_retry(runnable, payload, *, attempts: int | None = None) -> tuple[Any, LLMUsage]:
    budget = attempts or settings.LLM_MAX_ATTEMPTS
    started = time.monotonic()
    last: Exception | None = None

    for attempt in range(budget):
        try:
            result = runnable.invoke(payload)
        except Exception as exc:
            last = exc
            if not _is_rate_limited(exc):
                break
            if attempt + 1 < budget:
                time.sleep(2 ** attempt)
            continue

        elapsed_ms = int((time.monotonic() - started) * 1000)
        usage_model = settings.GEMINI_MODEL
        if isinstance(result, dict):
            return result.get("parsed"), LLMUsage(
                tokens=_read_usage(result.get("raw")),
                latency_ms=elapsed_ms,
                model=usage_model,
            )
        return result, LLMUsage(tokens=0, latency_ms=elapsed_ms, model=usage_model)

    raise LLMUnavailable(f"LLM call failed after {budget} attempt(s): {last}")
