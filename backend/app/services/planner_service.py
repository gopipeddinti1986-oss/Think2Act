from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.planner_repository import PlannerRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas.planner import (
    PlannerEntryCreate, PlannerEntryUpdate, PlannerEntryResponse,
    AutoScheduleResponse, AutoScheduleSuggestion
)

class PlannerService:
    def __init__(self, db: AsyncSession):
        self.planner_repo = PlannerRepository(db)
        self.task_repo = TaskRepository(db)
        self.user_repo = UserRepository(db)

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
        # Fetch user profile for work hours and preferred sprint duration
        user = await self.user_repo.get_by_id(user_id)
        work_start_str = (user.profile.work_start_time if user and user.profile and user.profile.work_start_time else "09:00")
        work_end_str = (user.profile.work_end_time if user and user.profile and user.profile.work_end_time else "18:00")
        preferred_sprint = (user.profile.preferred_sprint_minutes if user and user.profile and user.profile.preferred_sprint_minutes else 45)

        start_h, start_m = [int(p) for p in work_start_str.split(":")[:2]]
        end_h, end_m = [int(p) for p in work_end_str.split(":")[:2]]

        day_start = schedule_date.replace(hour=start_h, minute=start_m, second=0, microsecond=0)
        day_end = schedule_date.replace(hour=end_h, minute=end_m, second=0, microsecond=0)

        # Query existing planner entries on this day
        day_range_start = schedule_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_range_end = schedule_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        existing_entries = await self.planner_repo.list_by_user_and_range(user_id, day_range_start, day_range_end)

        occupied_slots: List[tuple] = []
        already_scheduled_task_ids = set()
        for e in existing_entries:
            if getattr(e, "status", None) != "CANCELLED":
                occupied_slots.append((e.start_at, e.end_at))
                if getattr(e, "task_id", None):
                    already_scheduled_task_ids.add(e.task_id)

        occupied_slots.sort(key=lambda x: x[0])

        # Calculate actual available hours
        total_work_minutes = max(0, int((day_end - day_start).total_seconds() / 60))
        booked_minutes = 0
        for s, e in occupied_slots:
            # Normalize naive/aware datetime comparison if needed
            s_cmp = s.replace(tzinfo=day_start.tzinfo) if (s.tzinfo and not day_start.tzinfo) or (not s.tzinfo and day_start.tzinfo) else s
            e_cmp = e.replace(tzinfo=day_end.tzinfo) if (e.tzinfo and not day_end.tzinfo) or (not e.tzinfo and day_end.tzinfo) else e
            overlap_start = max(day_start, s_cmp)
            overlap_end = min(day_end, e_cmp)
            if overlap_end > overlap_start:
                booked_minutes += int((overlap_end - overlap_start).total_seconds() / 60)

        available_minutes = max(0, total_work_minutes - booked_minutes)
        available_hours = round(available_minutes / 60.0, 1)

        # Get pending tasks
        pending_tasks = await self.task_repo.list_by_user(user_id, status="TODO")
        unscheduled_tasks = [
            t for t in pending_tasks 
            if t.id not in already_scheduled_task_ids and str(t.status) not in ("COMPLETED", "CANCELLED")
        ]

        priority_weight = {"URGENT": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        sorted_tasks = sorted(unscheduled_tasks, key=lambda t: priority_weight.get(t.priority, 1), reverse=True)

        suggestions: List[AutoScheduleSuggestion] = []
        total_planned_minutes = 0
        current_slot = day_start

        for task in sorted_tasks:
            duration = task.estimated_minutes or preferred_sprint
            dur_delta = timedelta(minutes=duration)

            # Advance current_slot past any overlapping occupied slots
            conflict = True
            while conflict:
                conflict = False
                for occ_start, occ_end in occupied_slots:
                    occ_s_cmp = occ_start.replace(tzinfo=current_slot.tzinfo) if (occ_start.tzinfo and not current_slot.tzinfo) or (not occ_start.tzinfo and current_slot.tzinfo) else occ_start
                    occ_e_cmp = occ_end.replace(tzinfo=current_slot.tzinfo) if (occ_end.tzinfo and not current_slot.tzinfo) or (not occ_end.tzinfo and current_slot.tzinfo) else occ_end
                    if max(current_slot, occ_s_cmp) < min(current_slot + dur_delta, occ_e_cmp):
                        current_slot = occ_e_cmp + timedelta(minutes=10)
                        conflict = True
                        break

            slot_end = current_slot + dur_delta
            if slot_end > day_end:
                break

            suggestions.append(AutoScheduleSuggestion(
                task_id=task.id,
                task_title=task.title,
                start_at=current_slot,
                end_at=slot_end,
                priority=task.priority
            ))
            total_planned_minutes += duration
            occupied_slots.append((current_slot, slot_end))
            occupied_slots.sort(key=lambda x: x[0])
            current_slot = slot_end + timedelta(minutes=15)

        total_planned_hours = round(total_planned_minutes / 60.0, 1)
        is_overloaded = (len(suggestions) < len(sorted_tasks)) or (total_planned_hours > available_hours)

        return AutoScheduleResponse(
            date=schedule_date.strftime("%Y-%m-%d"),
            available_hours=available_hours,
            total_planned_hours=total_planned_hours,
            is_overloaded=is_overloaded,
            suggestions=suggestions
        )

    async def generate_schedule_suggestions(
        self,
        user_id: Any,
        work_start: datetime,
        work_end: datetime
    ) -> dict:
        uid = UUID(str(user_id)) if not isinstance(user_id, UUID) else user_id
        pending_tasks = await self.task_repo.list_by_user(uid)
        active_tasks = [t for t in pending_tasks if str(t.status) not in ("COMPLETED", "CANCELLED")]

        existing_entries = await self.planner_repo.list_by_user_and_range(uid, work_start, work_end)
        occupied_slots = [(e.start_at, e.end_at) for e in existing_entries if getattr(e, "status", None) != "CANCELLED"]
        occupied_slots.sort(key=lambda x: x[0])
        already_scheduled_task_ids = {e.task_id for e in existing_entries if getattr(e, "task_id", None)}

        unscheduled_tasks = [t for t in active_tasks if t.id not in already_scheduled_task_ids]

        priority_weight = {"URGENT": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        sorted_tasks = sorted(
            unscheduled_tasks,
            key=lambda t: (
                priority_weight.get(str(getattr(t, "priority", "MEDIUM")), 2),
                -(t.due_at.timestamp() if getattr(t, "due_at", None) else 0)
            ),
            reverse=True
        )

        slots = []
        current_pointer = work_start
        for task in sorted_tasks:
            duration_mins = getattr(task, "estimated_minutes", None) or getattr(task, "estimated_duration_minutes", None) or 45
            dur = timedelta(minutes=duration_mins)

            conflict = True
            while conflict:
                conflict = False
                for occ_s, occ_e in occupied_slots:
                    s_cmp = occ_s.replace(tzinfo=current_pointer.tzinfo) if (occ_s.tzinfo and not current_pointer.tzinfo) or (not occ_s.tzinfo and current_pointer.tzinfo) else occ_s
                    e_cmp = occ_e.replace(tzinfo=current_pointer.tzinfo) if (occ_e.tzinfo and not current_pointer.tzinfo) or (not occ_e.tzinfo and current_pointer.tzinfo) else occ_e
                    if max(current_pointer, s_cmp) < min(current_pointer + dur, e_cmp):
                        current_pointer = e_cmp + timedelta(minutes=10)
                        conflict = True
                        break

            if current_pointer + dur > work_end:
                break
            slots.append({
                "task_id": str(task.id),
                "task_title": task.title,
                "priority": str(getattr(task, "priority", "MEDIUM")),
                "estimated_minutes": duration_mins,
                "proposed_start_time": current_pointer.isoformat(),
                "proposed_end_time": (current_pointer + dur).isoformat(),
                "reasoning": f"Prioritized for optimal execution block ({task.priority})"
            })
            occupied_slots.append((current_pointer, current_pointer + dur))
            occupied_slots.sort(key=lambda x: x[0])
            current_pointer += dur + timedelta(minutes=10)

        total_suggested_minutes = sum(s["estimated_minutes"] for s in slots)
        return {
            "total_suggested_minutes": total_suggested_minutes,
            "slots": slots
        }

    async def confirm_schedule_suggestions(
        self,
        user_id: Any,
        confirmed_slots: List[Any]
    ) -> dict:
        uid = UUID(str(user_id)) if not isinstance(user_id, UUID) else user_id
        scheduled_entries = []
        for slot in confirmed_slots:
            slot_dict = slot if isinstance(slot, dict) else (slot.model_dump() if hasattr(slot, "model_dump") else slot.__dict__)
            t_id = slot_dict.get("task_id")
            st_raw = slot_dict.get("proposed_start_time") or slot_dict.get("start_at")
            et_raw = slot_dict.get("proposed_end_time") or slot_dict.get("end_at")
            
            if isinstance(st_raw, str):
                start_at = datetime.fromisoformat(st_raw.replace("Z", "+00:00"))
            else:
                start_at = st_raw
                
            if isinstance(et_raw, str):
                end_at = datetime.fromisoformat(et_raw.replace("Z", "+00:00"))
            else:
                end_at = et_raw
            
            entry = await self.planner_repo.create(uid, PlannerEntryCreate(
                task_id=UUID(str(t_id)),
                start_at=start_at,
                end_at=end_at,
                status="SCHEDULED",
                source="AUTO"
            ))
            scheduled_entries.append(str(entry.id))
        return {"confirmed": len(scheduled_entries), "entry_ids": scheduled_entries}
