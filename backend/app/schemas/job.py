from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any

class JobPostingBase(BaseModel):
    title: str
    company: str
    location: str
    salary_range: Optional[str] = None
    description: Optional[str] = None
    required_skills: List[Dict[str, Any]] = []

class JobPostingCreate(JobPostingBase):
    pass

class JobPostingResponse(JobPostingBase):
    id: UUID
    match_percentage: float = 85.0
    missing_skills: List[str] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ApplicationEventCreate(BaseModel):
    event_type: str
    title: str
    notes: Optional[str] = None

class ApplicationEventResponse(BaseModel):
    id: UUID
    application_id: UUID
    event_type: str
    title: str
    notes: Optional[str] = None
    event_date: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class JobApplicationCreate(BaseModel):
    job_id: UUID
    status: str = "SAVED"
    notes: Optional[str] = None

class JobApplicationUpdateStatus(BaseModel):
    status: str

class JobApplicationResponse(BaseModel):
    id: UUID
    user_id: UUID
    job_id: UUID
    status: str
    applied_at: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    job: Optional[JobPostingResponse] = None
    events: List[ApplicationEventResponse] = []

    model_config = ConfigDict(from_attributes=True)
