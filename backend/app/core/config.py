from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv
import os

# Load .env from backend/ directory (one level up from app/)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str 

    # JWT
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # App
    APP_NAME: str = "aiTA - AI Teaching Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    # Set to an existing user's email to enable POST /auth/dev-login, which skips
    # the password and the OTP. Ignored unless DEBUG is also true.
    DEV_LOGIN_EMAIL: str = ""
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # ── Groq API Key for LLM agent reasoning ─────────────────────────────
    GROQ_API_KEY: str=""
    YOUTUBE_API_KEY: str=""

    # ── LLM (NVIDIA NIM) ──────────────────────────────────────────────────
    NVIDIA_API_KEY: str = ""
    # Two models, one provider. Most of the catalogue is already end of life and
    # available_models still lists the dead ones, so ping before switching either.
    #
    # Prose. Nemotron cannot write code into a JSON field: it strips the line
    # breaks out and the program becomes one unparseable line.
    NVIDIA_MODEL: str = "nvidia/nemotron-3-super-120b-a12b"
    # Code. The dedicated codegen model retired 2026-09-13 and nothing else on this
    # key writes code, so this is the chat model until a replacement exists. Only
    # bank-miss generation depends on it; seeded problems ship their own cases.
    NVIDIA_CODEGEN_MODEL: str = "nvidia/nemotron-3-super-120b-a12b"
    LLM_MAX_OUTPUT_TOKENS: int = 8192
    LLM_MAX_ATTEMPTS: int = 3

    # ── Code execution ────────────────────────────────────────────────────
    EXECUTION_PROVIDER: str = "sidecar"
    EXECUTOR_URL: str = "http://executor:8080"
    EXEC_WALL_SECONDS: float = 2.0
    EXEC_CPU_SECONDS: int = 2
    EXEC_MEMORY_MB: int = 256
    EXEC_MAX_PROCESSES: int = 64
    EXEC_OUTPUT_KB: int = 64
    EXEC_COMPILE_SECONDS: int = 10

    # ── Evaluation pipeline ───────────────────────────────────────────────
    EVAL_PIPELINE: str = "v2"
    TEST_CASES_MIN: int = 3
    TEST_CASES_TARGET: int = 8
    REFERENCE_MAX_ATTEMPTS: int = 3

    # ── Email (SMTP) for OTP delivery ─────────────────────────────────────
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "aiTA"
    
    # ── Gmail API (OAuth2 - works on Render via HTTPS) ────────────────────
    GMAIL_CLIENT_ID: str = ""
    GMAIL_CLIENT_SECRET: str = ""
    GMAIL_REFRESH_TOKEN: str = ""
    GMAIL_FROM_EMAIL: str = ""
    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
        extra = "ignore"
    

settings = Settings()