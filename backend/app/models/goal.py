import uuid
from sqlalchemy import Column, String, Date, Text, ForeignKey, Uuid
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimeStampedModel

class Goal(Base, TimeStampedModel):
    __tablename__ = "goals"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    priority = Column(String(50), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, URGENT
    status = Column(String(50), default="IN_PROGRESS", nullable=False)  # NOT_STARTED, IN_PROGRESS, COMPLETED, ON_HOLD
    start_date = Column(Date, nullable=True)
    target_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="goals")
    tasks = relationship("Task", back_populates="goal")
