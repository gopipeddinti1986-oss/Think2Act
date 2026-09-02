from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Float, JSON, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.core.database import Base

class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), default="CAREER")  # CAREER, PROJECT, TIME_ALLOCATION, TECHNICAL
    status = Column(String(50), default="DRAFT")  # DRAFT, EVALUATED, DECIDED
    recommended_option_id = Column(Uuid, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    options = relationship("DecisionOption", back_populates="decision", cascade="all, delete-orphan", lazy="selectin")
    criteria = relationship("DecisionCriterion", back_populates="decision", cascade="all, delete-orphan", lazy="selectin")

class DecisionOption(Base):
    __tablename__ = "decision_options"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    decision_id = Column(Uuid, ForeignKey("decisions.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    total_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    decision = relationship("Decision", back_populates="options")
    scores = relationship("DecisionScore", back_populates="option", cascade="all, delete-orphan", lazy="selectin")

class DecisionCriterion(Base):
    __tablename__ = "decision_criteria"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    decision_id = Column(Uuid, ForeignKey("decisions.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)  # Time, Risk, Effort, Career Impact, Compensation
    weight = Column(Float, default=1.0)  # 1.0 to 5.0
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    decision = relationship("Decision", back_populates="criteria")
    scores = relationship("DecisionScore", back_populates="criterion", cascade="all, delete-orphan", lazy="selectin")

class DecisionScore(Base):
    __tablename__ = "decision_scores"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    option_id = Column(Uuid, ForeignKey("decision_options.id", ondelete="CASCADE"), nullable=False, index=True)
    criterion_id = Column(Uuid, ForeignKey("decision_criteria.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, default=5.0)  # 1 to 10 scale
    rationale = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    option = relationship("DecisionOption", back_populates="scores")
    criterion = relationship("DecisionCriterion", back_populates="scores")
