import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Numeric, DateTime, Text, ForeignKey, Integer, PrimaryKeyConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimeStampedModel, utc_now

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=True)  # Software Engineering, Data & AI, Cloud, Security
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    role_skills = relationship("RoleSkill", back_populates="role", cascade="all, delete-orphan")

class RoleSkill(Base):
    __tablename__ = "role_skills"

    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    required_level = Column(Numeric(5, 2), default=70.0, nullable=False)  # Minimum target score (0-100)
    importance = Column(String(50), default="HIGH", nullable=False)        # HIGH, MEDIUM, LOW

    __table_args__ = (
        PrimaryKeyConstraint("role_id", "skill_id", name="pk_role_skills"),
    )

    role = relationship("Role", back_populates="role_skills")
    skill = relationship("Skill")

class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    provider = Column(String(100), nullable=True)  # Documentation, Coursera, LeetCode, FreeCodeCamp, Project Build
    url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    difficulty = Column(String(50), default="Intermediate", nullable=False)  # Beginner, Intermediate, Advanced
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    skills = relationship("LearningResourceSkill", back_populates="resource", cascade="all, delete-orphan")

class LearningResourceSkill(Base):
    __tablename__ = "learning_resource_skills"

    resource_id = Column(UUID(as_uuid=True), ForeignKey("learning_resources.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (
        PrimaryKeyConstraint("resource_id", "skill_id", name="pk_learning_resource_skills"),
    )

    resource = relationship("LearningResource", back_populates="skills")
    skill = relationship("Skill")

class LearningPath(Base, TimeStampedModel):
    __tablename__ = "learning_paths"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = Column(UUID(as_uuid=True), ForeignKey("goals.id", ondelete="SET NULL"), nullable=True, index=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    status = Column(String(50), default="ACTIVE", nullable=False)  # ACTIVE, COMPLETED, ARCHIVED

    user = relationship("User")
    goal = relationship("Goal")
    role = relationship("Role")
    items = relationship("LearningPathItem", back_populates="learning_path", cascade="all, delete-orphan", order_by="LearningPathItem.sequence_number")

class LearningPathItem(Base):
    __tablename__ = "learning_path_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learning_path_id = Column(UUID(as_uuid=True), ForeignKey("learning_paths.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    resource_id = Column(UUID(as_uuid=True), ForeignKey("learning_resources.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    sequence_number = Column(Integer, default=1, nullable=False)
    status = Column(String(50), default="PENDING", nullable=False)  # PENDING, IN_PROGRESS, COMPLETED
    progress = Column(Numeric(5, 2), default=0.0, nullable=False)   # 0.0 to 100.0
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    learning_path = relationship("LearningPath", back_populates="items")
    skill = relationship("Skill")
    resource = relationship("LearningResource")
