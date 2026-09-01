from typing import Optional, List
from uuid import UUID
from datetime import datetime, timezone, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from app.models.focus import FocusSession

class FocusRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, session_id: UUID, user_id: UUID) -> Optional[FocusSession]:
        stmt = (
            select(FocusSession)
            .options(selectinload(FocusSession.task))
            .where(FocusSession.id == session_id, FocusSession.user_id == user_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_session(self, user_id: UUID) -> Optional[FocusSession]:
        stmt = (
            select(FocusSession)
            .options(selectinload(FocusSession.task))
            .where(FocusSession.user_id == user_id, FocusSession.status.in_(["RUNNING", "PAUSED"]))
            .order_by(FocusSession.started_at.desc())
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List[FocusSession]:
        stmt = (
            select(FocusSession)
            .options(selectinload(FocusSession.task))
            .where(FocusSession.user_id == user_id)
            .order_by(FocusSession.started_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, user_id: UUID, task_id: Optional[UUID] = None) -> FocusSession:
        session = FocusSession(
            user_id=user_id,
            task_id=task_id,
            status="RUNNING"
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session, ["task"])
        return session

    async def finish(
        self,
        session_id: UUID,
        user_id: UUID,
        productive_seconds: int,
        distracted_seconds: int
    ) -> Optional[FocusSession]:
        session = await self.get_by_id(session_id, user_id)
        if not session:
            return None
        session.productive_seconds = productive_seconds
        session.distracted_seconds = distracted_seconds
        session.duration_seconds = productive_seconds + distracted_seconds
        session.ended_at = datetime.now(timezone.utc)
        session.status = "COMPLETED"
        await self.db.commit()
        await self.db.refresh(session, ["task"])
        return session

    async def get_today_totals(self, user_id: UUID):
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = select(
            func.count(FocusSession.id),
            func.coalesce(func.sum(FocusSession.productive_seconds), 0),
            func.coalesce(func.sum(FocusSession.distracted_seconds), 0)
        ).where(
            FocusSession.user_id == user_id,
            FocusSession.started_at >= today_start,
            FocusSession.status == "COMPLETED"
        )
        res = await self.db.execute(stmt)
        count, productive_s, distracted_s = res.first()
        total_s = productive_s + distracted_s
        ratio = (productive_s / total_s * 100) if total_s > 0 else 100.0
        return count, int(productive_s), int(distracted_s), round(ratio, 1)
