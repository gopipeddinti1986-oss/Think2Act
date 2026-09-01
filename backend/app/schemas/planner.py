from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from app.schemas.task import TaskResponse

class PlannerEntryBase(BaseModel):
    task_id: UUID
    start_at: datetime
    end_at: datetime
    status: str = "SCHEDULED" # SCHEDULED, COMPLETED, MISSED, CANCELLED
    source: str = "MANUAL"    # MANUAL, AUTO_SUGGESTED, AI_COACH

class PlannerEntryCreate(PlannerEntryBase):
    pass

class PlannerEntryUpdate(BaseModel):
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    status: Optional[str] = None

class PlannerEntryResponse(PlannerEntryBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    task: Optional[TaskResponse] = None

    class Config:
        from_attributes = True

class AutoScheduleSuggestion(BaseModel):
    task_id: UUID
    task_title: str
    start_at: datetime
    end_at: datetime
    priority: str

class AutoScheduleResponse(BaseModel):
    date: str
    available_hours: float
    total_planned_hours: float
    is_overloaded: bool
    suggestions: List[AutoScheduleSuggestion]
