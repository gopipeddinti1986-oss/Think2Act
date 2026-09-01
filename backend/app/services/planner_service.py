from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.planner_repository import PlannerRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.planner import (
    PlannerEntryCreate, PlannerEntryUpdate, PlannerEntryResponse,
    AutoScheduleResponse, AutoScheduleSuggestion
)

class PlannerService:
    def __init__(self, db: AsyncSession):
        self.planner_repo = PlannerRepository(db)
        self.task_repo = TaskRepository(db)

    async def list_entries(
        self,
        user_id: UUID,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[PlannerEntryResponse]:
        entries = await self.planner_repo.list_by_user_and_range(user_id, start_time, end_time)
        return [PlannerEntryResponse.model_validate(e) for e in entries]

    async def create_entry(self, user_id: UUID, data: PlannerEntryCreate) -> PlannerEntryResponse:
        # Verify task belongs to user
        task = await self.task_repo.get_by_id(data.task_id, user_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
        
        if data.end_at <= data.start_at:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="End time must be after start time.")

        entry = await self.planner_repo.create(user_id, data)
        return PlannerEntryResponse.model_validate(entry)

    async def update_entry(self, entry_id: UUID, user_id: UUID, data: PlannerEntryUpdate) -> PlannerEntryResponse:
        entry = await self.planner_repo.update(entry_id, user_id, data)
        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planner entry not found.")
        return PlannerEntryResponse.model_validate(entry)

    async def delete_entry(self, entry_id: UUID, user_id: UUID) -> dict:
        success = await self.planner_repo.delete(entry_id, user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planner entry not found.")
        return {"message": "Planner entry deleted successfully."}

    async def auto_schedule_suggestions(self, user_id: UUID, schedule_date: datetime) -> AutoScheduleResponse:
        # Get pending tasks
        pending_tasks = await self.task_repo.list_by_user(user_id, status="TODO")
        
        # Available work window: 9:00 AM to 6:00 PM (9 hours = 540 mins)
        day_start = schedule_date.replace(hour=9, minute=0, second=0, microsecond=0)
        current_slot = day_start
        available_hours = 6.0
        
        suggestions: List[AutoScheduleSuggestion] = []
        total_planned_minutes = 0

        # Sort tasks by priority (URGENT > HIGH > MEDIUM > LOW)
        priority_weight = {"URGENT": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        sorted_tasks = sorted(pending_tasks, key=lambda t: priority_weight.get(t.priority, 1), reverse=True)

        for task in sorted_tasks:
            duration = task.estimated_minutes or 45
            slot_end = current_slot + timedelta(minutes=duration)
            
            suggestions.append(AutoScheduleSuggestion(
                task_id=task.id,
                task_title=task.title,
                start_at=current_slot,
                end_at=slot_end,
                priority=task.priority
            ))
            total_planned_minutes += duration
            # 15 minute break between tasks
            current_slot = slot_end + timedelta(minutes=15)

        total_planned_hours = round(total_planned_minutes / 60.0, 1)
        is_overloaded = total_planned_hours > available_hours

        return AutoScheduleResponse(
            date=schedule_date.strftime("%Y-%m-%d"),
            available_hours=available_hours,
            total_planned_hours=total_planned_hours,
            is_overloaded=is_overloaded,
            suggestions=suggestions
        )
