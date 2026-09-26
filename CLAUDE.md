# fastapi-mastery

A learning project: FastAPI + SQLAlchemy 2.0 + Alembic + PostgreSQL, being grown
stage by stage into a RAG (Retrieval-Augmented Generation) application. The
person driving this is learning Python/FastAPI coming from a MERN/Next.js
background, so keep explanations beginner-friendly and avoid jargon without
context.

## Stack

- **FastAPI** — HTTP layer (routers)
- **SQLAlchemy 2.0** (`Mapped`/`mapped_column` style) — ORM
- **Alembic** — database migrations
- **PostgreSQL** — production/dev database
- **pydantic-settings** — config, loaded from `.env`
- **PyJWT** — access tokens
- **pwdlib[argon2]** — password hashing
- Tests use **pytest** + FastAPI's `TestClient` against a temporary SQLite
  database (never the real Postgres instance)

## Folder structure

Requests flow **routers → services → models/schemas**:

- `app/routers/` — HTTP endpoints only: parse request, call a service, return
  a response. No business logic or direct DB queries here.
- `app/services/` — business logic and DB queries (via SQLAlchemy `Session`).
  Routers call services; services don't know about HTTP.
- `app/models/` — SQLAlchemy ORM models (the DB table shape).
- `app/schemas/` — Pydantic models (the API request/response shape). Models
  and schemas are deliberately separate: the DB shape and the API contract
  are allowed to differ.
- `app/security.py` — password hashing and JWT creation.
- `app/dependencies.py` — FastAPI dependencies (`get_db`, `get_current_user`).
- `app/config.py` — `Settings`, loaded from `.env` via pydantic-settings.
- `alembic/` — migration scripts. `alembic/env.py` reads the DB URL from
  `Settings`, never hardcoded.

## Conventions

- **Secrets only ever live in `.env`** (gitignored). Never hardcode a DB
  password, JWT secret, or API key in source files or `alembic.ini`. Use
  `.env.example` to document what variables are needed, with placeholder
  values.
- **Every behavioral change needs a test.** Tests live in `tests/`, run
  against a temporary SQLite database created in `tests/conftest.py` (env
  vars are set there before the app is imported, so the real Postgres
  database is never touched).
- **Keep explanations beginner-friendly.** When describing a change, explain
  it simply, as if to someone new to Python — this person knows JS/TypeScript
  and React/Next.js, so analogies to that world are welcome.
- Passwords are always stored hashed (`hashed_password` column), never plain
  text.
- Don't restructure folders or rename things beyond what a task explicitly
  asks for.

## Roadmap: growing this into a RAG app

This project is being extended in stages. Expected upcoming stages (subject
to change — check recent commits/conversations for current status):

1. Document upload
2. Chunking
3. Embeddings with `pgvector`
4. An `/ask` endpoint with citations
5. Per-user retrieval (users only search their own documents)
6. Chat history
7. Hybrid search (keyword + vector)
8. Evaluation (measuring retrieval/answer quality)

Each stage should build on the auth foundation established in Stage 0 (this
stage): every new endpoint that touches user data should require
authentication via `get_current_user` and scope data access to the current
user, following the pattern in `app/routers/users.py`.
