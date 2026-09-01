# Think2Act Architecture & Engineering Blueprint

## Overview
Think2Act is designed as a **Modular Monolith** with clean boundaries between execution, intelligence, and career systems.

```
THINK2ACT
│
├── frontend/ (React + TypeScript + Vite + Tailwind CSS + TanStack Query)
│   ├── app/ (router, providers, config)
│   ├── components/ (layout, ui, common)
│   ├── features/ (auth, dashboard, goals, tasks, planner, focus, progress, skills, learning, jobs, resume, interviews, ai)
│   └── services/api/
│
└── backend/ (FastAPI + SQLAlchemy 2 + Alembic + PostgreSQL + Pydantic v2)
    ├── app/
    │   ├── core/ (config, security, database)
    │   ├── api/ (deps, v1/ [auth, users, dashboard, goals, tasks])
    │   ├── models/ (user, goal, task, ...)
    │   ├── schemas/ (pydantic validation)
    │   ├── repositories/ (isolated data access)
    │   ├── services/ (domain business logic)
    │   └── ai/ (isolated LLM orchestration & tools)
    ├── migrations/ (Alembic versioned DDL)
    └── tests/ (Pytest test suite)
```

## Security & Authorization
1. Every protected endpoint identifies the user from the verified JWT bearer token on the server. Client-provided `user_id` values are never trusted for authorization.
2. All database queries filter strictly by `user_id == current_user.id` to guarantee multi-tenant data isolation.
