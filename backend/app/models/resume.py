from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Float, JSON, Boolean, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.core.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    target_role = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=True)
    parsed_sections = Column(JSON, default=dict)  # {experience: [], skills: [], education: []}
    ats_score = Column(Float, default=70.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    suggestions = relationship("ResumeSuggestion", back_populates="resume", cascade="all, delete-orphan", lazy="selectin")

class ResumeSuggestion(Base):
    __tablename__ = "resume_suggestions"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    resume_id = Column(Uuid, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    section = Column(String(100), nullable=False)  # experience, summary, skills
    suggestion_type = Column(String(50), nullable=False)  # IMPACT_BULLET, MISSING_KEYWORD, QUANTIFIABLE_METRIC
    current_text = Column(Text, nullable=False)
    recommended_text = Column(Text, nullable=False)
    impact_reason = Column(Text, nullable=True)
    is_applied = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    resume = relationship("Resume", back_populates="suggestions")
