from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Float, JSON, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.core.database import Base

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    salary_range = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    required_skills = Column(JSON, default=list)  # list of {name, required_level}
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(Uuid, ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), default="SAVED")  # SAVED, APPLIED, OA, INTERVIEW, OFFER, REJECTED
    applied_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    job = relationship("JobPosting", lazy="joined")
    events = relationship("ApplicationEvent", back_populates="application", cascade="all, delete-orphan", lazy="selectin")

class ApplicationEvent(Base):
    __tablename__ = "application_events"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    application_id = Column(Uuid, ForeignKey("job_applications.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False)  # STATUS_CHANGE, OA_SCHEDULED, INTERVIEW_ROUND, OFFER_RECEIVED
    title = Column(String(255), nullable=False)
    notes = Column(Text, nullable=True)
    event_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    application = relationship("JobApplication", back_populates="events")
