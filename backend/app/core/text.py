import hashlib
import re

_WHITESPACE = re.compile(r"\s+")


def normalize_output(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def normalize_statement(text: str) -> str:
    return _WHITESPACE.sub(" ", text).strip().lower()


def statement_hash(text: str) -> str:
    return hashlib.sha256(normalize_statement(text).encode("utf-8")).hexdigest()


def truncate(text: str, limit_kb: int) -> tuple[str, bool]:
    limit = limit_kb * 1024
    encoded = text.encode("utf-8")
    if len(encoded) <= limit:
        return text, False
    return encoded[:limit].decode("utf-8", errors="ignore"), True
