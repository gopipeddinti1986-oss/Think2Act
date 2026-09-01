from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class EvidenceCreate(BaseModel):
    skill_id: UUID
    source_type: str = "MANUAL"  # PROJECT, CERTIFICATE, PROBLEM_SOLVING, TASK_EXECUTION, MANUAL
    source_id: Optional[UUID] = None
    strength: float = 15.0
    description: str

class EvidenceResponse(BaseModel):
    id: UUID
    user_id: UUID
    skill_id: UUID
    source_type: str
    source_id: Optional[UUID] = None
    strength: float
    description: str
    occurred_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
