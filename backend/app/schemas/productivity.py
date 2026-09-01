from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from typing import List, Optional

class ProductivitySnapshotResponse(BaseModel):
    id: UUID
    user_id: UUID
    date: date
    tasks_planned: int
    tasks_completed: int
    focus_seconds: int
    distraction_seconds: int
    score: float
    created_at: datetime

    class Config:
        from_attributes = True

class DailyMetricPoint(BaseModel):
    date: str
    score: float
    focus_minutes: int
    distraction_minutes: int
    tasks_completed: int

class ProductivityTrendResponse(BaseModel):
    current_score: float
    previous_score: float
    change_percentage: float
    range_days: int
    history: List[DailyMetricPoint]
    estimation_accuracy_percentage: float
    strongest_focus_period: str
