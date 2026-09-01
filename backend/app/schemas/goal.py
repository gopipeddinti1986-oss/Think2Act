from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from typing import Optional

class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: str = "MEDIUM" # LOW, MEDIUM, HIGH, URGENT
    status: str = "IN_PROGRESS" # NOT_STARTED, IN_PROGRESS, COMPLETED, ON_HOLD
    start_date: Optional[date] = None
    target_date: Optional[date] = None

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None

class GoalResponse(GoalBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
