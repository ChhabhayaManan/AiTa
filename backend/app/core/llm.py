import time
from dataclasses import dataclass
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
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


NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"


def get_chat_model(temperature: float = 0.0) -> ChatOpenAI:
    """Prose: feedback and explanations. NVIDIA's limits are far higher than the
    Gemini free tier, and its endpoint is OpenAI-compatible."""
    return ChatOpenAI(
        model=settings.NVIDIA_MODEL,
        api_key=settings.NVIDIA_API_KEY,
        base_url=NVIDIA_BASE_URL,
        temperature=temperature,
        max_completion_tokens=settings.LLM_MAX_OUTPUT_TOKENS,
        # Nemotron reasons before answering, and on a structured call it spends the
        # entire budget thinking and returns nothing to parse. Not optional.
        extra_body={"chat_template_kwargs": {"thinking": False}},
    )


def get_codegen_model(temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    """Code inside a JSON field, which is a stricter requirement than prose.

    Every NVIDIA model reachable on this key returns the program with its line
    breaks stripped, making it a single unparseable line. Plain completions from
    the same models are fine, so it is the structured-output path, not the model
    being weak. Gemini stays here until an NVIDIA model gets this right.
    """
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=temperature,
        max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS,
    )


def structured(model, schema: type[BaseModel]):
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


def invoke_with_retry(runnable, payload, *, attempts: int | None = None,
                      model: str | None = None) -> tuple[Any, LLMUsage]:
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
        usage_model = model or settings.NVIDIA_MODEL
        if isinstance(result, dict):
            return result.get("parsed"), LLMUsage(
                tokens=_read_usage(result.get("raw")),
                latency_ms=elapsed_ms,
                model=usage_model,
            )
        return result, LLMUsage(tokens=0, latency_ms=elapsed_ms, model=usage_model)

    raise LLMUnavailable(f"LLM call failed after {budget} attempt(s): {last}")
