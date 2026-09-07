from pydantic import BaseModel, ConfigDict, model_validator
from uuid import UUID
from datetime import datetime
from typing import Optional, Any

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
    source: str = "USER"      # USER, AI, LEARNING, SKILL_GAP, INTERVIEW, SYSTEM

    @model_validator(mode="before")
    def set_duration_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "estimated_duration_minutes" in data and "estimated_minutes" not in data:
                data["estimated_minutes"] = data["estimated_duration_minutes"]
            if "deadline" in data and "due_at" not in data:
                data["due_at"] = data["deadline"]
        return data

class TaskCreate(TaskBase):
    estimated_duration_minutes: Optional[int] = None
    deadline: Optional[datetime] = None

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
    source: Optional[str] = None

class TaskCompletePayload(BaseModel):
    actual_duration_minutes: Optional[int] = None
    actual_minutes: Optional[int] = None

class TaskResponse(TaskBase):
    id: UUID
    user_id: UUID
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
