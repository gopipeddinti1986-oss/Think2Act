import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimeStampedModel, utc_now

class AIConversation(Base, TimeStampedModel):
    __tablename__ = "ai_conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), default="New Coaching Session", nullable=False)

    user = relationship("User")
    messages = relationship("AIMessage", back_populates="conversation", cascade="all, delete-orphan", order_by="AIMessage.created_at")
    actions = relationship("AIAction", back_populates="conversation")

class AIMessage(Base):
    __tablename__ = "ai_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    conversation = relationship("AIConversation", back_populates="messages")

class AIAction(Base):
    __tablename__ = "ai_actions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("ai_conversations.id", ondelete="SET NULL"), nullable=True, index=True)
    action_type = Column(String(100), nullable=False)  # CREATE_TASK, SCHEDULE_TASK, COMPLETE_TASK, CREATE_LEARNING_ROADMAP
    target_type = Column(String(50), nullable=False)  # TASK, PLANNER, LEARNING
    target_id = Column(UUID(as_uuid=True), nullable=True)
    payload = Column(JSONB, nullable=True)             # Parameters proposed by AI
    status = Column(String(50), default="PENDING", nullable=False)  # PENDING, CONFIRMED, REJECTED, EXECUTED
    requires_confirmation = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    confirmed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User")
    conversation = relationship("AIConversation", back_populates="actions")
