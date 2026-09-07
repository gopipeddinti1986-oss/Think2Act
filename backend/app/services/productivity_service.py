from typing import List, Optional, Dict
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

        # Real estimation accuracy (actual vs estimated minutes across completed tasks)
        tasks = await self.task_repo.list_by_user(user_id, status="COMPLETED")
        accuracy = 0.0
        if tasks:
            diffs = []
            for t in tasks:
                if t.estimated_minutes > 0:
                    diff = abs(t.actual_minutes - t.estimated_minutes) / t.estimated_minutes
                    diffs.append(max(0.0, 1.0 - diff))
            if diffs:
                accuracy = round((sum(diffs) / len(diffs)) * 100, 1)

        # Real calculation of Peak Focus Time from user's actual focus sessions
        focus_sessions = await self.focus_repo.list_by_user(user_id, limit=100)
        if len(focus_sessions) < 3:
            peak_focus_time = f"Not enough data yet ({len(focus_sessions)}/3 focus sessions)"
        else:
            time_buckets: Dict[str, dict] = {
                "Morning": {"hours": "9 AM - 12 PM", "count": 0, "seconds": 0},
                "Afternoon": {"hours": "12 PM - 5 PM", "count": 0, "seconds": 0},
                "Evening": {"hours": "5 PM - 10 PM", "count": 0, "seconds": 0},
                "Night": {"hours": "10 PM - 6 AM", "count": 0, "seconds": 0},
            }
            for fs in focus_sessions:
                if fs.started_at:
                    hr = fs.started_at.hour
                    dur = fs.duration_seconds or 0
                    if 6 <= hr < 12:
                        bucket = "Morning"
                    elif 12 <= hr < 17:
                        bucket = "Afternoon"
                    elif 17 <= hr < 22:
                        bucket = "Evening"
                    else:
                        bucket = "Night"
                    time_buckets[bucket]["count"] += 1
                    time_buckets[bucket]["seconds"] += dur

            winner_name = max(time_buckets, key=lambda b: (time_buckets[b]["seconds"], time_buckets[b]["count"]))
            winner_info = time_buckets[winner_name]
            peak_focus_time = f"{winner_name} ({winner_info['hours']}) - based on {len(focus_sessions)} sessions"

        return ProductivityTrendResponse(
            range_days=days,
            average_score=round(avg_score, 1),
            total_focus_hours=round(total_focus_sec / 3600, 1),
            total_completed_tasks=total_tasks_comp,
            estimation_accuracy=accuracy,
            estimation_accuracy_percentage=accuracy,
            peak_focus_time=peak_focus_time,
            history=history_points
        )
