from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    goal_id: Optional[UUID] = None
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH, URGENT
    status: str = "TODO"      # TODO, IN_PROGRESS, COMPLETED, DEFERRED, CANCELLED
    due_at: Optional[datetime] = None
    estimated_minutes: int = 30
    actual_minutes: int = 0
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

class TaskResponse(TaskBase):
    id: UUID
    user_id: UUID
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
