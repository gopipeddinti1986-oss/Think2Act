from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.activity_repository import ActivityRepository
from app.schemas.activity import ActivityEventResponse

class ActivityService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ActivityRepository(db)

    async def log_event(
        self,
        user_id: UUID,
        event_type: str,
        title: str,
        description: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[UUID] = None,
        payload: Optional[Dict[str, Any]] = None
    ) -> ActivityEventResponse:
        event = await self.repo.create(
            user_id=user_id,
            event_type=event_type,
            title=title,
            description=description,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload
        )
        return ActivityEventResponse.model_validate(event)

    async def get_recent_activities(
        self,
        user_id: UUID,
        limit: int = 20,
        event_type: Optional[str] = None
    ) -> List[ActivityEventResponse]:
        events = await self.repo.list_by_user(user_id, event_type=event_type, limit=limit)
        return [ActivityEventResponse.model_validate(e) for e in events]
