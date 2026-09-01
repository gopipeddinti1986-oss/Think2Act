import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Numeric, DateTime, Text, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimeStampedModel, utc_now

class Skill(Base):
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=True)  # Programming, Backend, Database, Cloud, DSA
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    user_skills = relationship("UserSkill", back_populates="skill", cascade="all, delete-orphan")
    evidence_items = relationship("Evidence", back_populates="skill", cascade="all, delete-orphan")

class UserSkill(Base):
    __tablename__ = "user_skills"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    level = Column(Numeric(5, 2), default=0.0, nullable=False)  # 0 to 100.00
    confidence = Column(Numeric(5, 2), default=0.5, nullable=False)  # 0.0 to 1.0 (Low, Med, High)
    last_assessed_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "skill_id", name="pk_user_skills"),
    )

    user = relationship("User")
    skill = relationship("Skill", back_populates="user_skills")

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    source_type = Column(String(50), nullable=False)  # TASK_EXECUTION, PROJECT, CERTIFICATE, PROBLEM_SOLVING, MANUAL
    source_id = Column(UUID(as_uuid=True), nullable=True)
    strength = Column(Numeric(5, 2), default=10.0, nullable=False)  # Weight of this evidence item
    description = Column(Text, nullable=False)
    occurred_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    user = relationship("User")
    skill = relationship("Skill", back_populates="evidence_items")

    __table_args__ = (
        Index("idx_evidence_user_skill", "user_id", "skill_id"),
    )

class SkillHistory(Base):
    __tablename__ = "skill_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    level = Column(Numeric(5, 2), nullable=False)
    confidence = Column(Numeric(5, 2), nullable=False)
    reason = Column(String(255), nullable=True)
    recorded_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    user = relationship("User")
    skill = relationship("Skill")

    __table_args__ = (
        Index("idx_skill_history_user_skill", "user_id", "skill_id", "recorded_at"),
    )

class TaskSkill(Base):
    __tablename__ = "task_skills"

    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (
        PrimaryKeyConstraint("task_id", "skill_id", name="pk_task_skills"),
    )

    task = relationship("Task")
    skill = relationship("Skill")
