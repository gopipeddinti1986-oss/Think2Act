# Think2Act

Think2Act is a personal productivity + career-intelligence system built around one core loop:

```
GOAL → TASK → PLAN → FOCUS → COMPLETE → PROGRESS → EVIDENCE → SKILL → SKILL GAP → LEARNING → BETTER SKILL → BETTER JOB MATCH → APPLICATION → INTERVIEW → OUTCOME
```

## Milestone 1: Foundation + Core Execution Loop
- Authentication (Register, Login, Session via JWT)
- Goals CRUD & Tracking
- Tasks CRUD & Priority/Time estimation
- Unified Aggregate Dashboard (`GET /api/v1/dashboard`)
- Full-stack React + TypeScript + Tailwind CSS Frontend
- FastAPI + PostgreSQL + SQLAlchemy 2 + Alembic Backend

## Quick Start (Docker Compose)

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Interactive OpenAPI Docs: http://localhost:8000/docs
