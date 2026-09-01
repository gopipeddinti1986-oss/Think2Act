from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repository import TaskRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.evidence_repository import EvidenceRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = TaskRepository(db)
        self.skill_repo = SkillRepository(db)
        self.evidence_repo = EvidenceRepository(db)

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
        return TaskResponse.model_validate(task)

    async def update_task(self, task_id: UUID, user_id: UUID, data: TaskUpdate) -> TaskResponse:
        task = await self.repo.update(task_id, user_id, data)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
        return TaskResponse.model_validate(task)

    async def complete_task(self, task_id: UUID, user_id: UUID) -> TaskResponse:
        task = await self.repo.complete(task_id, user_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
        
        # Wire Milestone 3: Auto-generate evidence for associated skills
        from app.services.skill_service import SkillService
        skill_service = SkillService(self.db)
        await skill_service.on_task_completed(user_id, task.id, task.title)

        return TaskResponse.model_validate(task)

    async def delete_task(self, task_id: UUID, user_id: UUID) -> dict:
        success = await self.repo.delete(task_id, user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
        return {"message": "Task deleted successfully."}
