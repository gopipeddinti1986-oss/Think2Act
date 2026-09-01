from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.schemas.task import TaskResponse

class FocusSessionStart(BaseModel):
    task_id: Optional[UUID] = None

class FocusSessionFinish(BaseModel):
    productive_seconds: int
    distracted_seconds: int
    mark_task_completed: bool = False

class FocusSessionUpdate(BaseModel):
    productive_seconds: Optional[int] = None
    distracted_seconds: Optional[int] = None
    status: Optional[str] = None

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

    class Config:
        from_attributes = True

class FocusSummaryToday(BaseModel):
    total_sessions: int
    focus_seconds: int
    distracted_seconds: int
    focus_ratio: float
