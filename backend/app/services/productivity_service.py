from typing import List, Optional
from uuid import UUID
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.productivity_repository import ProductivityRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.focus_repository import FocusRepository
from app.schemas.productivity import (
    ProductivityTrendResponse, DailyMetricPoint, ProductivitySnapshotResponse
)

class ProductivityService:
    def __init__(self, db: AsyncSession):
        self.productivity_repo = ProductivityRepository(db)
        self.task_repo = TaskRepository(db)
        self.focus_repo = FocusRepository(db)

    async def get_progress_trends(self, user_id: UUID, days: int = 30) -> ProductivityTrendResponse:
        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)

        snapshots = await self.productivity_repo.list_range(user_id, start_date, end_date)
        snapshot_dict = {s.date: s for s in snapshots}

        history_points: List[DailyMetricPoint] = []
        for i in range(days):
            current_d = start_date + timedelta(days=i)
            if current_d in snapshot_dict:
                s = snapshot_dict[current_d]
                c_rate = (s.tasks_completed / s.tasks_planned * 100) if s.tasks_planned > 0 else 0.0
                history_points.append(DailyMetricPoint(
                    date=current_d.strftime("%b %d"),
                    score=float(s.score),
                    focus_minutes=int(s.focus_seconds / 60),
                    distraction_minutes=int(s.distraction_seconds / 60),
                    tasks_completed=s.tasks_completed,
                    completion_rate=round(c_rate, 1)
                ))
            else:
                history_points.append(DailyMetricPoint(
                    date=current_d.strftime("%b %d"),
                    score=0.0,
                    focus_minutes=0,
                    distraction_minutes=0,
                    tasks_completed=0,
                    completion_rate=0.0
                ))

        total_focus_sec = sum(s.focus_seconds for s in snapshots)
        total_tasks_comp = sum(s.tasks_completed for s in snapshots)
        avg_score = (sum(float(s.score) for s in snapshots) / len(snapshots)) if snapshots else 0.0

        # Calculate estimation accuracy (actual vs estimated minutes across completed tasks)
        tasks = await self.task_repo.list_by_user(user_id, status="COMPLETED")
        accuracy = 85.0  # default baseline
        if tasks:
            diffs = []
            for t in tasks:
                if t.estimated_minutes > 0:
                    diff = abs(t.actual_minutes - t.estimated_minutes) / t.estimated_minutes
                    diffs.append(max(0.0, 1.0 - diff))
            if diffs:
                accuracy = round((sum(diffs) / len(diffs)) * 100, 1)

        return ProductivityTrendResponse(
            range_days=days,
            average_score=round(avg_score, 1),
            total_focus_hours=round(total_focus_sec / 3600, 1),
            total_completed_tasks=total_tasks_comp,
            estimation_accuracy=accuracy,
            estimation_accuracy_percentage=accuracy,
            peak_focus_time="Morning (9 AM - 12 PM)",
            history=history_points
        )
