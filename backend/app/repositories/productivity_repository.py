from typing import Optional, List
from uuid import UUID
from datetime import date, datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from app.models.productivity import ProductivityMetric
from app.models.task import Task
from app.models.focus import FocusSession

class ProductivityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_date(self, user_id: UUID, metric_date: date) -> Optional[ProductivityMetric]:
        stmt = select(ProductivityMetric).where(
            ProductivityMetric.user_id == user_id,
            ProductivityMetric.date == metric_date
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_range(self, user_id: UUID, start_date: date, end_date: date) -> List[ProductivityMetric]:
        stmt = select(ProductivityMetric).where(
            ProductivityMetric.user_id == user_id,
            ProductivityMetric.date >= start_date,
            ProductivityMetric.date <= end_date
        ).order_by(ProductivityMetric.date.asc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def upsert_daily_snapshot(
        self,
        user_id: UUID,
        metric_date: date,
        tasks_planned: int,
        tasks_completed: int,
        focus_seconds: int,
        distraction_seconds: int,
        score: float
    ) -> ProductivityMetric:
        metric = await self.get_by_date(user_id, metric_date)
        if not metric:
            metric = ProductivityMetric(
                user_id=user_id,
                date=metric_date,
                tasks_planned=tasks_planned,
                tasks_completed=tasks_completed,
                focus_seconds=focus_seconds,
                distraction_seconds=distraction_seconds,
                score=score
            )
            self.db.add(metric)
        else:
            metric.tasks_planned = tasks_planned
            metric.tasks_completed = tasks_completed
            metric.focus_seconds = focus_seconds
            metric.distraction_seconds = distraction_seconds
            metric.score = score
        await self.db.commit()
        await self.db.refresh(metric)
        return metric
