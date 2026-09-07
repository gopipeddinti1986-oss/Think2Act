from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity import ActivityEvent

class ActivityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        user_id: UUID,
        event_type: str,
        title: str,
        description: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[UUID] = None,
        payload: Optional[Dict[str, Any]] = None,
        occurred_at: Optional[datetime] = None
    ) -> ActivityEvent:
        event = ActivityEvent(
            user_id=user_id,
            event_type=event_type,
            title=title,
            description=description,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload or {},
            occurred_at=occurred_at or datetime.now(timezone.utc)
        )
        self.db.add(event)
        await self.db.flush()
        return event

    create_event = create

    async def list_by_user(
        self,
        user_id: UUID,
        event_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[ActivityEvent]:
        query = (
            select(ActivityEvent)
            .where(ActivityEvent.user_id == user_id)
            .order_by(desc(ActivityEvent.occurred_at))
            .offset(offset)
            .limit(limit)
        )
        if event_type:
            query = query.where(ActivityEvent.event_type == event_type)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_by_user(
        self,
        user_id: UUID,
        event_type: Optional[str] = None,
        since: Optional[datetime] = None
    ) -> int:
        query = select(func.count(ActivityEvent.id)).where(ActivityEvent.user_id == user_id)
        if event_type:
            query = query.where(ActivityEvent.event_type == event_type)
        if since:
            query = query.where(ActivityEvent.occurred_at >= since)
        result = await self.db.execute(query)
        return result.scalar() or 0
