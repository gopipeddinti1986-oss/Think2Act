import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Index, Uuid
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimeStampedModel

class PlannerEntry(Base, TimeStampedModel):
    __tablename__ = "planner_entries"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    task_id = Column(Uuid, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    start_at = Column(DateTime(timezone=True), nullable=False)
    end_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), default="SCHEDULED", nullable=False)  # SCHEDULED, COMPLETED, MISSED, CANCELLED
    source = Column(String(50), default="MANUAL", nullable=False)    # MANUAL, AUTO_SUGGESTED, AI_COACH

    user = relationship("User")
    task = relationship("Task")

    __table_args__ = (
        Index("idx_planner_user_start", "user_id", "start_at"),
    )
