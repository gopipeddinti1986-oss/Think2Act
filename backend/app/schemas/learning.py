from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from app.schemas.skill import SkillResponse
from app.schemas.task import TaskResponse

class RoleSkillRequirement(BaseModel):
    skill_id: UUID
    skill_name: str
    required_level: float
    importance: str

class RoleResponse(BaseModel):
    id: UUID
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    requirements: List[RoleSkillRequirement] = []

    class Config:
        from_attributes = True

class SkillGapItem(BaseModel):
    skill_id: UUID
    skill_name: str
    category: Optional[str] = None
    current_level: float
    required_level: float
    gap: float
    importance: str
    severity: str  # CRITICAL, IMPORTANT, MODERATE, MINOR
    recommended_action: str

class SkillGapReport(BaseModel):
    role_id: UUID
    role_name: str
    overall_readiness: float
    total_gaps: int
    critical_gaps: int
    gaps: List[SkillGapItem]

class LearningResourceResponse(BaseModel):
    id: UUID
    title: str
    provider: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    difficulty: str

    class Config:
        from_attributes = True

class LearningPathItemResponse(BaseModel):
    id: UUID
    learning_path_id: UUID
    skill_id: UUID
    skill_name: Optional[str] = None
    title: str
    sequence_number: int
    status: str
    progress: float
    resource: Optional[LearningResourceResponse] = None

    class Config:
        from_attributes = True

class LearningPathResponse(BaseModel):
    id: UUID
    user_id: UUID
    goal_id: Optional[UUID] = None
    role_id: Optional[UUID] = None
    title: str
    status: str
    created_at: datetime
    items: List[LearningPathItemResponse] = []

    class Config:
        from_attributes = True

class GenerateRoadmapRequest(BaseModel):
    role_id: Optional[UUID] = None
    goal_id: Optional[UUID] = None
    title: Optional[str] = None

class ConvertLearningToTaskResponse(BaseModel):
    task: TaskResponse
    message: str
