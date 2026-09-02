import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Uuid
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimeStampedModel, utc_now

class User(Base, TimeStampedModel):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")

class UserProfile(Base, TimeStampedModel):
    __tablename__ = "user_profiles"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    organization = Column(String(255), nullable=True)
    education = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    user_mode = Column(String(50), default="student", nullable=False)  # student | employee
    career_goal = Column(Text, nullable=True)
    timezone = Column(String(100), default="UTC", nullable=False)

    user = relationship("User", back_populates="profile")
