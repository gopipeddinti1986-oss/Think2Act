from app.schemas.auth import (
    Token, TokenPayload, RegisterRequest, LoginRequest, AuthUserResponse, AuthResponse
)
from app.schemas.user import (
    UserProfileBase, UserProfileUpdate, UserProfileResponse, UserDetailResponse
)
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.dashboard import DashboardResponse, TasksSummary, AISuggestion

__all__ = [
    "Token", "TokenPayload", "RegisterRequest", "LoginRequest", "AuthUserResponse", "AuthResponse",
    "UserProfileBase", "UserProfileUpdate", "UserProfileResponse", "UserDetailResponse",
    "GoalCreate", "GoalUpdate", "GoalResponse",
    "TaskCreate", "TaskUpdate", "TaskResponse",
    "DashboardResponse", "TasksSummary", "AISuggestion"
]
