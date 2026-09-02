from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any

class DecisionScoreResponse(BaseModel):
    id: UUID
    option_id: UUID
    criterion_id: UUID
    score: float
    rationale: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DecisionCriterionResponse(BaseModel):
    id: UUID
    decision_id: UUID
    name: str
    weight: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DecisionOptionResponse(BaseModel):
    id: UUID
    decision_id: UUID
    name: str
    description: Optional[str] = None
    total_score: float
    created_at: datetime
    scores: List[DecisionScoreResponse] = []

    model_config = ConfigDict(from_attributes=True)

class DecisionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str = "CAREER"
    options: List[str] = []
    criteria: List[Dict[str, Any]] = []

class UpdateOptionScoreRequest(BaseModel):
    option_id: UUID
    criterion_id: UUID
    score: float
    rationale: Optional[str] = None

class DecisionResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    category: str
    status: str
    recommended_option_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    options: List[DecisionOptionResponse] = []
    criteria: List[DecisionCriterionResponse] = []

    model_config = ConfigDict(from_attributes=True)
