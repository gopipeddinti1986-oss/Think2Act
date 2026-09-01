import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import utc_now

class FocusSession(Base):
    __tablename__ = "focus_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True, index=True)
    started_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, default=0, nullable=False)
    productive_seconds = Column(Integer, default=0, nullable=False)
    distracted_seconds = Column(Integer, default=0, nullable=False)
    status = Column(String(50), default="RUNNING", nullable=False)  # RUNNING, PAUSED, COMPLETED, CANCELLED
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    user = relationship("User")
    task = relationship("Task")

    __table_args__ = (
        Index("idx_focus_user_started_at", "user_id", "started_at"),
    )
