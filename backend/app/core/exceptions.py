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


class SessionNotFound(AitaError):
    """A Content Player session that does not exist, or is not this user's.

    One exception for both so a caller cannot tell the two apart: answering
    differently would let a student probe for other people's session ids.
    """

    status_code = 404


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
