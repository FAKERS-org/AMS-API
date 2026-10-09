# AMS API

Asynchronous RESTful API for Academic Management System built with FastAPI, SQLAlchemy 2.0 (Asyncio), PostgreSQL, and Pydantic v2.

## Requirements

- Python 3.12+
- Docker & Docker Compose
- [uv](https://docs.astral.sh/uv/)

## Getting Started

### 1. Environment
```bash
cp .env.example .env
```

### 2. Database
```bash
docker compose up -d
```

### 3. Dependencies
```bash
uv sync
```

### 4. Migrations & Seeding
```bash
# Apply migrations
uv run alembic upgrade head

# (Optional) Seed users
uv run python -m app.database.main
```

### 5. Run Server
```bash
uv run uvicorn app.main:app --reload --port 8000
```

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

