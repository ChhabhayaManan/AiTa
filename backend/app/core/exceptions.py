from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AitaError(Exception):
    status_code = 500

    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


class SubmissionNotFound(AitaError):
    status_code = 404


class ProblemNotFound(AitaError):
    status_code = 404


class ThreadNotFound(AitaError):
    """A chat thread that does not exist or is not this user's: one answer for both,
    so thread ids cannot be probed."""

    status_code = 404


class TurnInProgress(AitaError):
    status_code = 409


class ExecutorUnavailable(AitaError):
    status_code = 503


class LLMUnavailable(AitaError):
    status_code = 503


class LanguageNotExecutable(AitaError):
    status_code = 422


class UnverifiableSubmission(AitaError):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AitaError)
    def handle(_: Request, exc: AitaError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
