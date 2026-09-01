from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.goals import router as goals_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.planner import router as planner_router
from app.api.v1.focus import router as focus_router
from app.api.v1.progress import router as progress_router
from app.api.v1.skills import router as skills_router
from app.api.v1.evidence import router as evidence_router
from app.api.v1.roles import router as roles_router
from app.api.v1.learning import router as learning_router
from app.api.v1.ai import router as ai_router
from app.api.v1.health import router as health_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(goals_router, prefix="/goals", tags=["Goals"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(planner_router, prefix="/planner", tags=["Planner"])
api_router.include_router(focus_router, prefix="/focus", tags=["Focus"])
api_router.include_router(progress_router, prefix="/progress", tags=["Progress"])
api_router.include_router(skills_router, prefix="/skills", tags=["Skills"])
api_router.include_router(evidence_router, prefix="/evidence", tags=["Evidence"])
api_router.include_router(roles_router, prefix="/roles", tags=["Roles"])
api_router.include_router(learning_router, prefix="/learning", tags=["Learning"])
api_router.include_router(ai_router, prefix="/ai", tags=["AI Coach"])
