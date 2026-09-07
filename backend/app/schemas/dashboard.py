from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from app.schemas.auth import AuthUserResponse
from app.schemas.goal import GoalResponse
from app.schemas.task import TaskResponse

class TasksSummary(BaseModel):
    total: int
    completed: int
    pending: int
    completion_rate: int

class AISuggestion(BaseModel):
    title: str
    message: str
    action_label: Optional[str] = None
    action_type: Optional[str] = None

class TodayExecution(BaseModel):
    tasks_completed: int = 0
    focus_minutes: int = 0
    schedule_count: int = 0

class DashboardResponse(BaseModel):
    user: AuthUserResponse
    tasks_summary: TasksSummary
    today_execution: Optional[TodayExecution] = None
    productivity_score: int
    focus_minutes_today: int
    readiness_score: int
    next_action: Optional[TaskResponse] = None
    today_tasks: List[TaskResponse]
    goals: List[GoalResponse]
    ai_suggestion: Optional[AISuggestion] = None
