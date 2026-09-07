import enum
import uuid
from sqlalchemy import Column, String, Date, Text, ForeignKey, Uuid
from sqlalchemy.orm import relationship, attributes
from app.core.database import Base
from app.models.base import TimeStampedModel

class PriorityEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class GoalStatus(str, enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"

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
    tasks = relationship("Task", back_populates="goal", lazy="selectin")

    @property
    def calculated_progress(self) -> float:
        # Check if tasks relationship is loaded without triggering async IO lazy load
        state = attributes.instance_state(self)
        if "tasks" in state.dict and state.dict["tasks"] is not None:
            tasks_list = state.dict["tasks"]
            if not tasks_list:
                return 100.0 if str(self.status) in ("COMPLETED", "GoalStatus.COMPLETED") else 0.0
            completed = sum(1 for t in tasks_list if str(t.status) in ("COMPLETED", "TaskStatus.COMPLETED"))
            return round((completed / len(tasks_list)) * 100.0, 1)
        return 100.0 if str(self.status) in ("COMPLETED", "GoalStatus.COMPLETED") else 0.0

    @property
    def health(self) -> str:
        progress = self.calculated_progress
        if progress >= 75.0 or str(self.status) in ("COMPLETED", "GoalStatus.COMPLETED"):
            return "HEALTHY"
        elif progress >= 30.0:
            return "AT_RISK"
        return "CRITICAL"
