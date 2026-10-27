
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.models import code_eval as code_eval_models, problem as problem_models  # noqa: F401
from app.api import auth, users, problems, code_eval, feedback, profile, assessment, chat, gamification
from app.api import onboarding, practice_sessions
from app.services.onboarding import pending
from app.services.rag import embedder


@asynccontextmanager
async def lifespan(app: FastAPI):
    # No create_all here. It adds missing tables but never missing columns, so a
    # database behind a migration starts up looking healthy and fails later on the
    # first write. Alembic owns the schema: run `alembic upgrade head`.
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} is running.")
    if not settings.SKIP_EMBED_WARMUP:
        embedder.warm_up_in_background()
    stop = asyncio.Event()
    sweep = None
    if not settings.SKIP_ONBOARDING_SWEEP:
        sweep = asyncio.create_task(pending.run_sweep_loop(stop))
    yield
    stop.set()
    if sweep is not None:
        await sweep
    print("👋 Shutting down aiTA backend.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## aiTA — AI-Powered Teaching Assistant Backend

Practice, graded code, hints, feedback and a learner model per topic and language.

### Authentication
Use `/auth/login` to get a Bearer token, then click **Authorize**.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # open during deployment — tighten after it works
    allow_credentials=False,      # must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(problems.router, prefix="/api/v1")
app.include_router(code_eval.router,prefix="/api/v1")
app.include_router(feedback.router, prefix="/api/v1")
app.include_router(profile.router, prefix="/api/v1")
app.include_router(assessment.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(gamification.router, prefix="/api/v1")
app.include_router(onboarding.router, prefix="/api/v1")
app.include_router(practice_sessions.router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def root():
    return {"app": settings.APP_NAME, "version": settings.APP_VERSION, "status": "running", "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}