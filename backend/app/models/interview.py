from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Float, JSON, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.core.database import Base

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_title = Column(String(255), nullable=False)
    session_type = Column(String(50), default="TECHNICAL")  # TECHNICAL, SYSTEM_DESIGN, BEHAVIORAL
    status = Column(String(50), default="IN_PROGRESS")  # IN_PROGRESS, COMPLETED
    overall_score = Column(Float, default=0.0)
    summary_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    questions = relationship("InterviewQuestion", back_populates="session", cascade="all, delete-orphan", lazy="selectin")

class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    session_id = Column(Uuid, ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    target_skill = Column(String(100), nullable=True)
    difficulty = Column(String(50), default="MEDIUM")
    user_answer = Column(Text, nullable=True)
    rubric_scores = Column(JSON, default=dict)  # {correctness: 80, clarity: 90, completeness: 85}
    ai_feedback = Column(Text, nullable=True)
    ideal_answer = Column(Text, nullable=True)
    score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    session = relationship("InterviewSession", back_populates="questions")
