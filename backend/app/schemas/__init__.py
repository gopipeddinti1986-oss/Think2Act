from app.schemas.auth import (
    Token, TokenPayload, RegisterRequest, LoginRequest, AuthUserResponse, AuthResponse
)
from app.schemas.user import (
    UserProfileBase, UserProfileUpdate, UserProfileResponse, UserDetailResponse
)
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.dashboard import DashboardResponse, TasksSummary, AISuggestion
from app.schemas.planner import (
    PlannerEntryCreate, PlannerEntryUpdate, PlannerEntryResponse,
    AutoScheduleRequest, AutoScheduleResponse, AutoScheduleSuggestion
)
from app.schemas.focus import (
    FocusSessionStart, FocusSessionFinish, FocusSessionUpdate,
    FocusSessionResponse, FocusSummaryToday
)
from app.schemas.productivity import (
    ProductivitySnapshotResponse, DailyMetricPoint, ProductivityTrendResponse
)
from app.schemas.skill import (
    SkillCreate, SkillResponse, UserSkillResponse, EvidenceItemResponse,
    SkillHistoryPoint, AssignTaskSkillsRequest
)
from app.schemas.evidence import EvidenceCreate, EvidenceResponse

__all__ = [
    "Token", "TokenPayload", "RegisterRequest", "LoginRequest", "AuthUserResponse", "AuthResponse",
    "UserProfileBase", "UserProfileUpdate", "UserProfileResponse", "UserDetailResponse",
    "GoalCreate", "GoalUpdate", "GoalResponse",
    "TaskCreate", "TaskUpdate", "TaskResponse",
    "DashboardResponse", "TasksSummary", "AISuggestion",
    "PlannerEntryCreate", "PlannerEntryUpdate", "PlannerEntryResponse",
    "AutoScheduleRequest", "AutoScheduleResponse", "AutoScheduleSuggestion",
    "FocusSessionStart", "FocusSessionFinish", "FocusSessionUpdate",
    "FocusSessionResponse", "FocusSummaryToday",
    "ProductivitySnapshotResponse", "DailyMetricPoint", "ProductivityTrendResponse",
    "SkillCreate", "SkillResponse", "UserSkillResponse", "EvidenceItemResponse",
    "SkillHistoryPoint", "AssignTaskSkillsRequest",
    "EvidenceCreate", "EvidenceResponse"
]
