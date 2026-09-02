from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any

class InterviewQuestionResponse(BaseModel):
    id: UUID
    session_id: UUID
    question_text: str
    target_skill: Optional[str] = None
    difficulty: str
    user_answer: Optional[str] = None
    rubric_scores: Dict[str, Any] = {}
    ai_feedback: Optional[str] = None
    ideal_answer: Optional[str] = None
    score: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class InterviewSessionCreate(BaseModel):
    role_title: str = "Backend Software Engineer"
    session_type: str = "TECHNICAL"

class SubmitAnswerRequest(BaseModel):
    question_id: UUID
    answer: str

class InterviewSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    role_title: str
    session_type: str
    status: str
    overall_score: float
    summary_feedback: Optional[str] = None
    created_at: datetime
    questions: List[InterviewQuestionResponse] = []

    model_config = ConfigDict(from_attributes=True)
