import uuid
from datetime import date, datetime, timezone
from sqlalchemy import Column, Integer, Numeric, Date, DateTime, ForeignKey, Index, UniqueConstraint, Uuid
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import utc_now

class ProductivityMetric(Base):
    __tablename__ = "productivity_metrics"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, default=date.today, nullable=False)
    tasks_planned = Column(Integer, default=0, nullable=False)
    tasks_completed = Column(Integer, default=0, nullable=False)
    focus_seconds = Column(Integer, default=0, nullable=False)
    distraction_seconds = Column(Integer, default=0, nullable=False)
    score = Column(Numeric(5, 2), default=0.0, nullable=False)  # 0 to 100.00
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    user = relationship("User")

    __table_args__ = (
        UniqueConstraint("user_id", "date", name="uq_user_date_productivity"),
        Index("idx_productivity_user_date", "user_id", "date"),
    )
