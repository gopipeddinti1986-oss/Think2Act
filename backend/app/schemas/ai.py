from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any

class AIMessageBase(BaseModel):
    role: str  # user, assistant, system
    content: str

class AIMessageCreate(AIMessageBase):
    pass

class AIMessageResponse(AIMessageBase):
    id: UUID
    conversation_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AIActionBase(BaseModel):
    action_type: str  # CREATE_TASK, SCHEDULE_TASK, COMPLETE_TASK, CREATE_ROADMAP
    target_type: str  # TASK, PLANNER, LEARNING
    target_id: Optional[UUID] = None
    payload: Optional[Dict[str, Any]] = None
    requires_confirmation: bool = True

class AIActionResponse(AIActionBase):
    id: UUID
    user_id: UUID
    conversation_id: Optional[UUID] = None
    status: str  # PENDING, CONFIRMED, REJECTED, EXECUTED
    created_at: datetime
    confirmed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class AIConversationResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[AIMessageResponse] = []
    actions: List[AIActionResponse] = []

    model_config = ConfigDict(from_attributes=True)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None

from pydantic import BaseModel, ConfigDict, model_validator

class ChatResponse(BaseModel):
    conversation_id: UUID
    message: AIMessageResponse
    proposed_actions: List[AIActionResponse] = []
    reply: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def set_reply_field(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get("reply") and "message" in data:
                msg = data["message"]
                if hasattr(msg, "content"):
                    data["reply"] = msg.content
                elif isinstance(msg, dict) and "content" in msg:
                    data["reply"] = msg["content"]
        elif hasattr(data, "message") and not getattr(data, "reply", None):
            setattr(data, "reply", getattr(data.message, "content", ""))
        return data
