from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any

class ResumeSuggestionResponse(BaseModel):
    id: UUID
    resume_id: UUID
    section: str
    suggestion_type: str
    current_text: str
    recommended_text: str
    impact_reason: Optional[str] = None
    is_applied: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ResumeCreate(BaseModel):
    title: str
    target_role: str
    raw_text: Optional[str] = None
    parsed_sections: Optional[Dict[str, Any]] = None

class ResumeResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    target_role: str
    raw_text: Optional[str] = None
    parsed_sections: Dict[str, Any] = {}
    ats_score: float
    created_at: datetime
    updated_at: datetime
    suggestions: List[ResumeSuggestionResponse] = []

    model_config = ConfigDict(from_attributes=True)

class ApplySuggestionRequest(BaseModel):
    apply: bool = True
