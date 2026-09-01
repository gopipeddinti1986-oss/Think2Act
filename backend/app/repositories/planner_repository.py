from typing import Optional, List
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.models.planner import PlannerEntry
from app.schemas.planner import PlannerEntryCreate, PlannerEntryUpdate

class PlannerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, entry_id: UUID, user_id: UUID) -> Optional[PlannerEntry]:
        stmt = (
            select(PlannerEntry)
            .options(selectinload(PlannerEntry.task))
            .where(PlannerEntry.id == entry_id, PlannerEntry.user_id == user_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user_and_range(
        self,
        user_id: UUID,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[PlannerEntry]:
        conditions = [PlannerEntry.user_id == user_id]
        if start_time:
            conditions.append(PlannerEntry.start_at >= start_time)
        if end_time:
            conditions.append(PlannerEntry.start_at <= end_time)

        stmt = (
            select(PlannerEntry)
            .options(selectinload(PlannerEntry.task))
            .where(and_(*conditions))
            .order_by(PlannerEntry.start_at.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, user_id: UUID, data: PlannerEntryCreate) -> PlannerEntry:
        entry = PlannerEntry(
            user_id=user_id,
            **data.model_dump()
        )
        self.db.add(entry)
        await self.db.commit()
        await self.db.refresh(entry, ["task"])
        return entry

    async def update(self, entry_id: UUID, user_id: UUID, data: PlannerEntryUpdate) -> Optional[PlannerEntry]:
        entry = await self.get_by_id(entry_id, user_id)
        if not entry:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for key, val in update_data.items():
            setattr(entry, key, val)
        await self.db.commit()
        await self.db.refresh(entry, ["task"])
        return entry

    async def delete(self, entry_id: UUID, user_id: UUID) -> bool:
        entry = await self.get_by_id(entry_id, user_id)
        if not entry:
            return False
        await self.db.delete(entry)
        await self.db.commit()
        return True
