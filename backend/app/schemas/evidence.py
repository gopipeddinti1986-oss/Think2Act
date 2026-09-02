from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class EvidenceCreate(BaseModel):
    skill_id: UUID
    source_type: str = "PROJECT"  # TASK_EXECUTION, PROJECT, CERTIFICATE, PROBLEM_SOLVING, MANUAL
    source_id: Optional[UUID] = None
    strength: float = 10.0
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

    model_config = ConfigDict(from_attributes=True)
