from typing import List, Optional
from pydantic import BaseModel, Field

class JobRequirementItem(BaseModel):
    skill_name: str
    required_proficiency: float = Field(ge=0.0, le=100.0)
    is_mandatory: bool = True

class JobPostingCreate(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    salary_range: Optional[str] = None
    description: str
    requirements: List[JobRequirementItem]

class JobMatchScoreResponse(BaseModel):
    job_id: int
    job_title: str
    company: str
    overall_match_percentage: float
    matching_strengths: List[str]
    missing_gaps: List[str]
    recommendation: str