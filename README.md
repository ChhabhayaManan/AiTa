# aiTA — AI Teaching Assistant

A practice platform for first-year programming students in **C**, **C++** and **Python**.
Every answer is graded by running code or by a fixed key, never by a language model's
opinion. The grade updates a per-topic, per-language learner model, and that model picks
the next question.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What a student does

| Page | What happens |
|---|---|
| **Onboarding** (`/onboarding`) | Background questions, then a short diagnostic (MCQ, predict-the-output, fill-the-blank, find-the-bug, write-code, theory). Sets the starting level for each of the 12 topics. |
| **Practice** (`/practice`) | One question at a time: MCQ, debug challenge or coding problem, chosen from the weakest topic. Each answer is graded, moves the topic level, and counts toward a bounded session with a summary page at the end. |
| **Code workspace** (`/code-help`) | Generate a problem on a topic, write code, run it against hidden tests in a sandbox. A hint ladder (concept → steps → line pointer) is grounded in the failing attempt. After passing, or after **I give up**, the reference solution opens in the student's language. |
| **Code evaluation** (`/code-eval`) | Paste any code and a problem statement; tests are generated, validated against a reference, and run. |
| **Feedback** (`/feedback`) | Reports built from the latest evaluation and recent practice: errors, misconceptions, next topics. |
| **Language check** (`/language-check`) | Switching language triggers a short re-check so mastery in one language is not assumed in another. |
| **Chat** | A tutor chatbot grounded in course books (RAG), with moderation that nudges rather than blocks. |

Points, streaks and badges are computed from the event log and are replayable
(`GAMIFICATION_MODE`, default `silent`).

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, CodeMirror |
| Backend | FastAPI, SQLAlchemy, Alembic, LangGraph |
| Database | PostgreSQL with pgvector |
| LLM | NVIDIA NIM (Nemotron), through one gateway (`app/core/llm_gateway.py`) with per-purpose models, deadlines and a fallback model |
| Code execution | Self-hosted sandbox container (`backend/executor`) on an internal-only network |
| Auth | JWT (access + refresh), bcrypt, email OTP (Gmail API or SMTP) |

---

## Repository layout

```
AiTa/
├── docker-compose.yml          # executor + backend + frontend; DB from backend/.env
├── docker-compose.local.yml    # override: local pgvector Postgres on host port 5433
├── backend/
│   ├── executor/               # sandbox service that compiles and runs student code
│   ├── scripts/                # seeding, review, demo reset, metrics
│   ├── tests/                  # pytest (SQLite, no live LLM calls)
│   └── app/
│       ├── main.py             # FastAPI app, routers, startup tasks
│       ├── core/               # config, database, security, llm_gateway
│       ├── models/             # SQLAlchemy models
│       ├── schemas/            # Pydantic request/response models
│       ├── api/                # routers (one per area, below)
│       ├── agents/             # LangGraph graphs: assessment, chat, code_eval, feedback, profiling
│       ├── services/           # business logic: execution, test_generation, problems,
│       │                       #   hints, profiling, gamification, onboarding, rag, ...
│       ├── data/               # problem, diagnostic and practice banks; language guides
│       └── alembic/            # migrations (Alembic owns the schema)
└── frontend/
    └── src/
        ├── App.jsx             # routes
        ├── pages/              # one file per route
        ├── components/         # UI per feature, plus ui/ primitives
        ├── hooks/
        └── utils/api.js        # Axios client with token refresh
```

---

## Running it

### With Docker

`backend/.env` must exist first (see [Environment variables](#environment-variables)).

```bash
# local Postgres (recommended for development)
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d --build

# or against the database in backend/.env
docker compose up -d --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API docs | http://localhost:8000/docs |
| Executor | no published port, by design |

Apply migrations inside the backend container:

```bash
docker compose exec backend sh -c "cd /app/app && PYTHONPATH=/app alembic upgrade head"
```

> **Keep the `exec` flag** on the executor's tmpfs mount. Docker mounts tmpfs `noexec`
> by default, which breaks every compiled submission with "Permission denied".

### Seeding

Run inside the backend container (`docker compose exec backend python -m scripts.<name>`;
add `-f docker-compose.local.yml` when using the local DB). All are safe to rerun.

| Script | Loads |
|---|---|
| `ingest_problems` | Problem bank with its own test cases (no API key needed) |
| `seed_practice` | Hand-written MCQ and debug items in C, C++ and Python, each proven by execution |
| `seed_assessments` | Verified assessment bank |
| `seed_diagnostic` | Onboarding diagnostic bank; approve items with `review_diagnostic` |
| `ingest_books` | Course-book chunks for the chatbot's retrieval |
| `rebuild_awards` | Rebuilds the gamification ledger from `learning_events` |
| `reset_demo_user` | Wipes and re-registers one demo account |
| `report_metrics` | Hint leak rate, verified correctness, mastery trace |

### Logging in without email

With no Gmail or SMTP credentials, OTPs are printed to the backend log:

```bash
docker compose logs backend | grep "\[DEV\] OTP"
```

Set `DEV_LOGIN_EMAIL` to an existing user's email and keep `DEBUG=True` to get a
**Dev login** button. With either missing, `POST /auth/dev-login` returns 404.

### Without Docker

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

cd app
PYTHONPATH=.. alembic upgrade head
cd ..
uvicorn app.main:app --reload --port 8000
```

`alembic.ini` lives in `backend/app` with a relative `script_location`, so run Alembic
from there. Startup does not create tables; migrating is the only way the schema changes.

Code execution still needs the sandbox. Publish it yourself and point the backend at it:

```bash
docker compose run -d --service-ports -p 8080:8080 executor
# backend/.env: EXECUTOR_URL=http://localhost:8080
```

Frontend:

```bash
cd frontend
npm install
npm run dev        # http://localhost:3000, proxies /api to :8000
```

---

## Tests and checks

```bash
# backend
cd backend
.venv\Scripts\python -m pytest -q
.venv\Scripts\python -m ruff check app tests

# frontend
cd frontend
npm run lint
npm test
npm run build
```

Backend tests run on SQLite with a fake execution provider and stubbed LLM calls, so
they need neither Docker nor an API key.

---

## Environment variables

Defined in `backend/app/core/config.py`. Unknown keys in `.env` are ignored.

| Variable | Required | Notes |
|---|---|---|
| `DATABASE_URL` | yes | PostgreSQL with pgvector |
| `SECRET_KEY` | yes | JWT signing secret |
| `NVIDIA_API_KEY` | for LLM features | Without it, LLM features degrade (e.g. pattern-only feedback, Python fallback solutions) |
| `NVIDIA_MODEL`, `NVIDIA_CODEGEN_MODEL`, `NVIDIA_FALLBACK_MODEL` | no | Model per purpose; see comments in `config.py` |
| `NVIDIA_RPM`, `LLM_QUEUE_DEADLINE_S`, `REDIS_URL` | no | Rate limiting and queueing |
| `EXECUTOR_URL` | no | Default `http://executor:8080` |
| `EXEC_*` | no | Sandbox limits: wall time, CPU, memory, processes, output, compile time |
| `GAMIFICATION_MODE` | no | `silent` (default) records awards without showing them |
| `DEV_LOGIN_EMAIL` | no | Enables the dev login button when `DEBUG=True` |
| `ALLOWED_ORIGINS` | no | CORS origins, comma-separated |
| `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`, `GMAIL_FROM_EMAIL` | no | OTP email via Gmail API |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` | no | OTP email via SMTP |
| `SKIP_EMBED_WARMUP`, `SKIP_ONBOARDING_SWEEP` | no | Skip startup background tasks |

---

## API

All routes are under `/api/v1`. Full interactive docs: `http://localhost:8000/docs`.

| Prefix | Purpose |
|---|---|
| `/auth` | Register, 2-step login with OTP, refresh, forgot/reset password, dev login |
| `/users` | Profile, consent, peer comparison, password change |
| `/onboarding` | Steps, diagnostic, finish, language switch and re-check |
| `/assessment` | Next practice item, MCQ answers, debug submissions |
| `/practice-sessions` | Current session, finish, summary, session feedback |
| `/problems` | Generate a problem; open its solution after a pass or a give-up |
| `/code-eval` | Submit code, run tests, history and stats |
| `/feedback` | Hint ladder, feedback reports |
| `/profile` | Mastery for every topic |
| `/gamification` | Points, streaks, badges |
| `/chat` | Tutor chat threads and messages |

---

## License

MIT — see [LICENSE](LICENSE).
