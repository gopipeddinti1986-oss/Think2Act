from typing import Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.tools.base import BaseTool, ToolResult
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate

class CreateTaskTool(BaseTool):
    name = "create_task"
    description = "Propose creating a new task targeting user career milestones or daily execution."
    parameters = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Title of the task"},
            "description": {"type": "string", "description": "Optional detailed instructions"},
            "priority": {"type": "string", "enum": ["URGENT", "HIGH", "MEDIUM", "LOW"], "default": "MEDIUM"},
            "estimated_minutes": {"type": "integer", "description": "Estimated duration in minutes", "default": 45},
            "category": {"type": "string", "description": "Task category e.g. DSA, Learning, System Design"}
        },
        "required": ["title"]
    }

    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_repo = TaskRepository(db)

    async def execute(self, user_id: UUID, params: Dict[str, Any], confirmed: bool = False) -> ToolResult:
        title = params.get("title")
        if not title:
            return ToolResult(
                success=False,
                action_type="CREATE_TASK",
                target_type="TASK",
                payload={},
                message="Task title is required."
            )

        priority = params.get("priority", "MEDIUM")
        estimated_minutes = params.get("estimated_minutes", 45)
        category = params.get("category", "General")
        desc = params.get("description", "")

        # Guardrail: Requires explicit user confirmation
        if not confirmed:
            return ToolResult(
                success=True,
                requires_confirmation=True,
                action_type="CREATE_TASK",
                target_type="TASK",
                payload={
                    "title": title,
                    "description": desc,
                    "priority": priority,
                    "estimated_minutes": estimated_minutes,
                    "category": category
                },
                message=f"I propose creating the task '{title}' ({priority} Priority, {estimated_minutes} min). Confirm to add it to your tasks."
            )

        # Execution when confirmed
        task = await self.task_repo.create(
            user_id=user_id,
            data=TaskCreate(
                title=title,
                description=desc,
                priority=priority,
                estimated_minutes=estimated_minutes,
                category=category,
                status="TODO"
            )
        )
        return ToolResult(
            success=True,
            requires_confirmation=False,
            action_type="CREATE_TASK",
            target_type="TASK",
            target_id=task.id,
            payload={"task_id": str(task.id), "title": task.title},
            message=f"Task '{task.title}' has been successfully created."
        )