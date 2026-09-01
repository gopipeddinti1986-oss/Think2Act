from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.goals import router as goals_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.health import router as health_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(goals_router, prefix="/goals", tags=["Goals"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
