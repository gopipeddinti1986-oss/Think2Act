from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any

class ActivityEventResponse(BaseModel):
    id: UUID
    user_id: UUID
    event_type: str
    title: str
    description: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    payload: Dict[str, Any] = {}
    occurred_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
