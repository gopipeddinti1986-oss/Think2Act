from typing import Dict, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.tools.base import BaseTool, ToolResult
from app.repositories.task_repository import TaskRepository
from app.repositories.planner_repository import PlannerRepository
from app.schemas.planner import PlannerEntryCreate

class ScheduleTaskTool(BaseTool):
    name = "schedule_task"
    description = "Propose scheduling an existing task into a specific time slot on the user's planner."
    parameters = {
        "type": "object",
        "properties": {
            "task_id": {"type": "string", "description": "UUID of the task to schedule"},
            "start_at": {"type": "string", "description": "ISO format start datetime"},
            "end_at": {"type": "string", "description": "ISO format end datetime"},
            "reason": {"type": "string", "description": "Reasoning for the scheduled window"}
        },
        "required": ["task_id", "start_at", "end_at"]
    }

    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_repo = TaskRepository(db)
        self.planner_repo = PlannerRepository(db)

    async def execute(self, user_id: UUID, params: Dict[str, Any], confirmed: bool = False) -> ToolResult:
        task_id_str = params.get("task_id")
        start_at_str = params.get("start_at")
        end_at_str = params.get("end_at")

        if not task_id_str or not start_at_str or not end_at_str:
            return ToolResult(
                success=False,
                action_type="SCHEDULE_TASK",
                target_type="PLANNER",
                payload={},
                message="task_id, start_at, and end_at are required to schedule a task."
            )

        task_id = UUID(task_id_str) if not isinstance(task_id_str, UUID) else task_id_str
        task = await self.task_repo.get_by_id(task_id, user_id)
        if not task:
            return ToolResult(
                success=False,
                action_type="SCHEDULE_TASK",
                target_type="PLANNER",
                payload={},
                message=f"Task {task_id_str} not found."
            )

        start_at = datetime.fromisoformat(start_at_str.replace("Z", "+00:00"))
        end_at = datetime.fromisoformat(end_at_str.replace("Z", "+00:00"))

        # Guardrail: Requires explicit user confirmation
        if not confirmed:
            return ToolResult(
                success=True,
                requires_confirmation=True,
                action_type="SCHEDULE_TASK",
                target_type="PLANNER",
                target_id=task.id,
                payload={
                    "task_id": str(task.id),
                    "task_title": task.title,
                    "start_at": start_at.isoformat(),
                    "end_at": end_at.isoformat(),
                    "reason": params.get("reason", "Priority execution window")
                },
                message=f"I propose scheduling '{task.title}' from {start_at.strftime('%H:%M')} to {end_at.strftime('%H:%M')}. Confirm to place it in your calendar."
            )

        # Execution when confirmed
        entry = await self.planner_repo.create(
            user_id=user_id,
            data=PlannerEntryCreate(
                task_id=task.id,
                start_at=start_at,
                end_at=end_at,
                status="SCHEDULED",
                source="AI_COACH"
            )
        )
        return ToolResult(
            success=True,
            requires_confirmation=False,
            action_type="SCHEDULE_TASK",
            target_type="PLANNER",
            target_id=entry.id,
            payload={"entry_id": str(entry.id), "task_id": str(task.id)},
            message=f"Task '{task.title}' has been scheduled for {start_at.strftime('%b %d at %H:%M')}."
        )