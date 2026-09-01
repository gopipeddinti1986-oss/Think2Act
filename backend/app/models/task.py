import uuid
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimeStampedModel

class Task(Base, TimeStampedModel):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    goal_id = Column(UUID(as_uuid=True), ForeignKey("goals.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(50), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, URGENT
    status = Column(String(50), default="TODO", nullable=False)      # TODO, IN_PROGRESS, COMPLETED, DEFERRED, CANCELLED
    due_at = Column(DateTime(timezone=True), nullable=True)
    estimated_minutes = Column(Integer, default=30, nullable=False)
    actual_minutes = Column(Integer, default=0, nullable=False)
    category = Column(String(100), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="tasks")
    goal = relationship("Goal", back_populates="tasks")

    __table_args__ = (
        Index("idx_tasks_user_status", "user_id", "status"),
        Index("idx_tasks_user_due_at", "user_id", "due_at"),
    )
