from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    goal_id: Optional[UUID] = None
    priority: str = "MEDIUM" # LOW, MEDIUM, HIGH, URGENT
    status: str = "TODO"     # TODO, IN_PROGRESS, COMPLETED, DEFERRED, CANCELLED
    due_at: Optional[datetime] = None
    estimated_minutes: int = 30
    category: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    goal_id: Optional[UUID] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_at: Optional[datetime] = None
    estimated_minutes: Optional[int] = None
    actual_minutes: Optional[int] = None
    category: Optional[str] = None
    completed_at: Optional[datetime] = None

class TaskResponse(TaskBase):
    id: UUID
    user_id: UUID
    actual_minutes: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
