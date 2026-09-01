from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone, date
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.focus_repository import FocusRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.productivity_repository import ProductivityRepository
from app.schemas.focus import (
    FocusSessionStart, FocusSessionFinish, FocusSessionResponse, FocusSummaryToday
)

class FocusService:
    def __init__(self, db: AsyncSession):
        self.focus_repo = FocusRepository(db)
        self.task_repo = TaskRepository(db)
        self.productivity_repo = ProductivityRepository(db)

    async def start_session(self, user_id: UUID, data: FocusSessionStart) -> FocusSessionResponse:
        # Check active session
        active = await self.focus_repo.get_active_session(user_id)
        if active:
            return FocusSessionResponse.model_validate(active)

        if data.task_id:
            task = await self.task_repo.get_by_id(data.task_id, user_id)
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
            if task.status == "TODO":
                task.status = "IN_PROGRESS"
                await self.task_repo.db.commit()

        session = await self.focus_repo.create(user_id, data.task_id)
        return FocusSessionResponse.model_validate(session)

    async def get_active_session(self, user_id: UUID) -> Optional[FocusSessionResponse]:
        session = await self.focus_repo.get_active_session(user_id)
        if not session:
            return None
        return FocusSessionResponse.model_validate(session)

    async def finish_session(
        self,
        session_id: UUID,
        user_id: UUID,
        data: FocusSessionFinish
    ) -> FocusSessionResponse:
        session = await self.focus_repo.finish(
            session_id=session_id,
            user_id=user_id,
            productive_seconds=data.productive_seconds,
            distracted_seconds=data.distracted_seconds
        )
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Focus session not found.")

        # Update task if completed or update actual duration
        if session.task_id:
            task = await self.task_repo.get_by_id(session.task_id, user_id)
            if task:
                task.actual_minutes += int(data.productive_seconds / 60)
                if data.mark_task_completed:
                    task.status = "COMPLETED"
                    task.completed_at = datetime.now(timezone.utc)
                await self.task_repo.db.commit()

        # Update Daily Productivity Snapshot
        today = date.today()
        total, completed, pending, rate = await self.task_repo.get_summary_counts(user_id)
        _, today_focus_s, today_distract_s, focus_ratio = await self.focus_repo.get_today_totals(user_id)
        
        # Weighted Productivity Score = 0.5 * (Task Completion Rate) + 0.5 * (Focus Ratio)
        productivity_score = round(0.5 * rate + 0.5 * focus_ratio, 1)

        await self.productivity_repo.upsert_daily_snapshot(
            user_id=user_id,
            metric_date=today,
            tasks_planned=total,
            tasks_completed=completed,
            focus_seconds=today_focus_s,
            distraction_seconds=today_distract_s,
            score=productivity_score
        )

        return FocusSessionResponse.model_validate(session)

    async def list_sessions(self, user_id: UUID) -> List[FocusSessionResponse]:
        sessions = await self.focus_repo.list_by_user(user_id)
        return [FocusSessionResponse.model_validate(s) for s in sessions]

    async def get_today_summary(self, user_id: UUID) -> FocusSummaryToday:
        count, focus_s, distract_s, ratio = await self.focus_repo.get_today_totals(user_id)
        return FocusSummaryToday(
            total_sessions=count,
            focus_seconds=focus_s,
            distracted_seconds=distract_s,
            focus_ratio=ratio
        )
