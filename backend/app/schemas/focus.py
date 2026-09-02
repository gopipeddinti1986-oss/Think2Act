from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.schemas.task import TaskResponse

class FocusSessionStart(BaseModel):
    task_id: Optional[UUID] = None

class FocusSessionUpdate(BaseModel):
    duration_seconds: int
    productive_seconds: int
    distracted_seconds: int
    status: Optional[str] = None

class FocusSessionFinish(BaseModel):
    productive_seconds: int
    distracted_seconds: int
    complete_task: bool = False
    mark_task_completed: bool = False

class FocusSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    task_id: Optional[UUID] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_seconds: int
    productive_seconds: int
    distracted_seconds: int
    status: str
    created_at: datetime
    task: Optional[TaskResponse] = None

    model_config = ConfigDict(from_attributes=True)

class FocusSummaryToday(BaseModel):
    total_sessions: int = 0
    total_focus_seconds: int = 0
    focus_seconds: int = 0
    total_distraction_seconds: int = 0
    distracted_seconds: int = 0
    focus_percentage: float = 0.0
    focus_ratio: float = 0.0
    is_active: bool = False
    active_session: Optional[FocusSessionResponse] = None

    model_config = ConfigDict(from_attributes=True)
