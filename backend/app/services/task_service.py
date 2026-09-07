from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repository import TaskRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.evidence_repository import EvidenceRepository
from app.repositories.activity_repository import ActivityRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = TaskRepository(db)
        self.skill_repo = SkillRepository(db)
        self.evidence_repo = EvidenceRepository(db)
        self.activity_repo = ActivityRepository(db)

    async def list_tasks(
        self,
        user_id: UUID,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        goal_id: Optional[UUID] = None,
        category: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[TaskResponse]:
        tasks = await self.repo.list_by_user(
            user_id=user_id,
            status=status,
            priority=priority,
            goal_id=goal_id,
            category=category,
            limit=limit,
            offset=offset
        )
        return [TaskResponse.model_validate(t) for t in tasks]

    async def get_task(self, task_id: UUID, user_id: UUID) -> TaskResponse:
        task = await self.repo.get_by_id(task_id, user_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
        return TaskResponse.model_validate(task)

    async def create_task(self, user_id: UUID, data: TaskCreate) -> TaskResponse:
        task = await self.repo.create(user_id, data)
        await self.activity_repo.create(
            user_id=user_id,
            event_type="TASK_CREATED",
            title=f"Created Task: {task.title}",
            description=task.description,
            entity_type="task",
            entity_id=task.id,
            payload={
                "priority": task.priority,
                "category": task.category,
                "source": task.source,
                "goal_id": str(task.goal_id) if task.goal_id else None
            }
        )
        await self.db.commit()
        return TaskResponse.model_validate(task)

    async def update_task(self, task_id: UUID, user_id: UUID, data: TaskUpdate) -> TaskResponse:
        task = await self.repo.update(task_id, user_id, data)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
        return TaskResponse.model_validate(task)

    async def complete_task(
        self,
        task_id: UUID,
        user_id: UUID,
        actual_duration_minutes: Optional[int] = None
    ) -> TaskResponse:
        """
        Completes a task atomically:
        1. Updates task status to COMPLETED and sets completion timestamp.
        2. Sets actual execution duration.
        3. Generates verified evidence for all associated skills.
        4. Recalculates skill scores with diminishing returns.
        5. Logs an immutable ActivityEvent.
        All operations are committed in a single atomic database transaction.
        """
        try:
            task = await self.repo.complete(task_id, user_id, commit=False)
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

            if actual_duration_minutes is not None:
                task.actual_minutes = actual_duration_minutes
                await self.db.flush()

            # Wire Evidence Graph for linked skills within the same transaction
            from app.services.skill_service import SkillService
            skill_service = SkillService(self.db)
            await skill_service.on_task_completed(user_id, task.id, task.title, commit=False)

            # Log Activity Event
            await self.activity_repo.create(
                user_id=user_id,
                event_type="TASK_COMPLETED",
                title=f"Completed Task: {task.title}",
                description=f"Logged {task.actual_minutes} minutes of execution time.",
                entity_type="task",
                entity_id=task.id,
                payload={
                    "actual_minutes": task.actual_minutes,
                    "estimated_minutes": task.estimated_minutes,
                    "goal_id": str(task.goal_id) if task.goal_id else None
                }
            )

            # Single atomic commit
            await self.db.commit()
            await self.db.refresh(task)
            return TaskResponse.model_validate(task)

        except Exception:
            await self.db.rollback()
            raise

    async def delete_task(self, task_id: UUID, user_id: UUID) -> dict:
        success = await self.repo.delete(task_id, user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
        return {"message": "Task deleted successfully."}
