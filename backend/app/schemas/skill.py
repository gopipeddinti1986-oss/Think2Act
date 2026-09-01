from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class SkillBase(BaseModel):
    name: str
    category: Optional[str] = "Programming"
    description: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class EvidenceItemResponse(BaseModel):
    id: UUID
    skill_id: UUID
    source_type: str
    source_id: Optional[UUID] = None
    strength: float
    description: str
    occurred_at: datetime

    class Config:
        from_attributes = True

class SkillHistoryPoint(BaseModel):
    level: float
    confidence: float
    reason: Optional[str] = None
    recorded_at: datetime

    class Config:
        from_attributes = True

class UserSkillResponse(BaseModel):
    skill_id: UUID
    name: str
    category: Optional[str] = None
    level: float
    confidence: float
    last_assessed_at: datetime
    evidence_count: int = 0
    recent_evidence: List[EvidenceItemResponse] = []
    history: List[SkillHistoryPoint] = []

    class Config:
        from_attributes = True

class AssignTaskSkillsRequest(BaseModel):
    skill_ids: List[UUID]
