import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Uuid, Index
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import utc_now

class ActivityEvent(Base):
    __tablename__ = "activity_events"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    entity_type = Column(String(50), nullable=True)
    entity_id = Column(Uuid, nullable=True)
    payload = Column(JSON, default=dict, nullable=False)
    occurred_at = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    user = relationship("User")

    __table_args__ = (
        Index("idx_activity_events_user_occurred", "user_id", "occurred_at"),
    )
