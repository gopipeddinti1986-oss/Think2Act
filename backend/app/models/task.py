import enum
import uuid
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Uuid, Index, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimeStampedModel

class TaskStatus(str, enum.Enum):
    TODO = "TODO"
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    DEFERRED = "DEFERRED"
    CANCELLED = "CANCELLED"

class Task(Base, TimeStampedModel):
    __tablename__ = "tasks"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    goal_id = Column(Uuid, ForeignKey("goals.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(50), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, URGENT
    status = Column(String(50), default="TODO", nullable=False)      # TODO, IN_PROGRESS, COMPLETED, DEFERRED, CANCELLED
    due_at = Column(DateTime(timezone=True), nullable=True)
    estimated_minutes = Column(Integer, default=30, nullable=False)
    actual_minutes = Column(Integer, default=0, nullable=False)
    category = Column(String(100), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    dependencies = Column(JSON, default=list, nullable=True)
    source = Column(String(50), default="USER", nullable=False)  # USER, AI, LEARNING, SKILL_GAP, INTERVIEW, SYSTEM

    user = relationship("User", back_populates="tasks")
    goal = relationship("Goal", back_populates="tasks")

    @property
    def estimated_duration_minutes(self) -> int:
        return self.estimated_minutes if self.estimated_minutes is not None else 30

    @estimated_duration_minutes.setter
    def estimated_duration_minutes(self, val: int):
        self.estimated_minutes = val

    @property
    def actual_duration_minutes(self) -> int:
        return self.actual_minutes if self.actual_minutes is not None else 0

    @actual_duration_minutes.setter
    def actual_duration_minutes(self, val: int):
        self.actual_minutes = val

    @property
    def deadline(self):
        return self.due_at

    @deadline.setter
    def deadline(self, val):
        self.due_at = val

    __table_args__ = (
        Index("idx_tasks_user_status", "user_id", "status"),
        Index("idx_tasks_user_due_at", "user_id", "due_at"),
    )
