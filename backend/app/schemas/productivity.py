from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List, Optional

class ProductivitySnapshotResponse(BaseModel):
    date: date
    tasks_planned: int
    tasks_completed: int
    focus_seconds: int
    distraction_seconds: int
    score: float

    model_config = ConfigDict(from_attributes=True)

class DailyMetricPoint(BaseModel):
    date: str
    score: float
    focus_minutes: int
    distraction_minutes: int
    tasks_completed: int
    completion_rate: float = 0.0

    model_config = ConfigDict(from_attributes=True)

class ProductivityTrendResponse(BaseModel):
    range_days: int
    average_score: float
    total_focus_hours: float
    total_completed_tasks: int
    estimation_accuracy: float
    estimation_accuracy_percentage: float
    peak_focus_time: Optional[str] = "Morning (9 AM - 12 PM)"
    history: List[DailyMetricPoint]

    model_config = ConfigDict(from_attributes=True)
