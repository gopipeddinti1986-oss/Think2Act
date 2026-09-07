from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# --- Base Skill Schemas ---
class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None

class SkillResponse(SkillBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- User Skill & Evidence Schemas ---
class UserSkillResponse(BaseModel):
    id: int
    user_id: int
    skill_id: int
    skill_name: str
    proficiency_level: float
    evidence_count: int
    last_demonstrated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserSkillCreate(BaseModel):
    skill_id: int
    proficiency_level: Optional[float] = 1.0

class UserSkillUpdate(BaseModel):
    proficiency_level: Optional[float] = None

class EvidenceCreate(BaseModel):
    skill_id: Optional[int] = None
    skill_name: Optional[str] = None
    source_type: str
    source_id: Optional[str] = None
    description: str
    weight: float = 1.0

class EvidenceItemResponse(BaseModel):
    id: int
    user_id: int
    skill_id: Optional[int] = None
    skill_name: Optional[str] = None
    source_type: str
    source_id: Optional[str] = None
    description: str
    weight: float = 1.0
    created_at: datetime

    class Config:
        from_attributes = True

# --- Skill History Schemas ---
class SkillHistoryPoint(BaseModel):
    timestamp: datetime
    proficiency_level: float
    source_type: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class SkillHistoryResponse(BaseModel):
    skill_id: int
    skill_name: str
    history: List[SkillHistoryPoint]

# --- Task Skill Assignment Schemas ---
class TaskSkillAssociation(BaseModel):
    skill_id: Optional[int] = None
    skill_name: Optional[str] = None
    weight: float = 1.0

class AssignTaskSkillsRequest(BaseModel):
    task_id: int
    skill_ids: Optional[List[int]] = None
    skills: Optional[List[TaskSkillAssociation]] = None

# --- Skill Gap & Role Requirement Schemas ---
class TargetRoleSkillRequirement(BaseModel):
    skill_id: Optional[int] = None
    skill_name: Optional[str] = None
    required_proficiency: float = 1.0
    importance: Optional[str] = "REQUIRED"

    class Config:
        from_attributes = True

class SkillGapItem(BaseModel):
    skill_id: Optional[int] = None
    skill_name: str
    required_level: float = 1.0
    current_level: float = 0.0
    gap: float = 1.0

class SkillGapAnalysisResponse(BaseModel):
    role_id: Optional[int] = None
    role_title: str
    overall_match_percentage: float
    missing_skills: List[SkillGapItem] = []
    matching_skills: List[SkillGapItem] = []