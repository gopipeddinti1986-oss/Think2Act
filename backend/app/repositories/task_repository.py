from typing import Optional, List
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, case
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        goal_id: Optional[UUID] = None,
        category: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Task]:
        conditions = [Task.user_id == user_id]
        if status:
            conditions.append(Task.status == status)
        if priority:
            conditions.append(Task.priority == priority)
        if goal_id:
            conditions.append(Task.goal_id == goal_id)
        if category:
            conditions.append(Task.category == category)

        stmt = select(Task).where(and_(*conditions)).order_by(
            Task.due_at.asc().nullslast(),
            Task.created_at.desc()
        ).limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, user_id: UUID, data: TaskCreate) -> Task:
        task = Task(
            user_id=user_id,
            **data.model_dump()
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def update(self, task_id: UUID, user_id: UUID, data: TaskUpdate) -> Optional[Task]:
        task = await self.get_by_id(task_id, user_id)
        if not task:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for key, val in update_data.items():
            setattr(task, key, val)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def complete(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        task = await self.get_by_id(task_id, user_id)
        if not task:
            return None
        task.status = "COMPLETED"
        task.completed_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task_id: UUID, user_id: UUID) -> bool:
        task = await self.get_by_id(task_id, user_id)
        if not task:
            return False
        await self.db.delete(task)
        await self.db.commit()
        return True

    async def get_summary_counts(self, user_id: UUID):
        total_stmt = select(func.count(Task.id)).where(Task.user_id == user_id)
        completed_stmt = select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.status == "COMPLETED"
        )
        
        total_res = await self.db.execute(total_stmt)
        completed_res = await self.db.execute(completed_stmt)
        
        total = total_res.scalar() or 0
        completed = completed_res.scalar() or 0
        pending = total - completed
        rate = int((completed / total) * 100) if total > 0 else 0
        return total, completed, pending, rate

    async def get_next_action(self, user_id: UUID) -> Optional[Task]:
        priority_weight = case(
            (Task.priority == "URGENT", 4),
            (Task.priority == "HIGH", 3),
            (Task.priority == "MEDIUM", 2),
            (Task.priority == "LOW", 1),
            else_=0
        )
        stmt = select(Task).where(
            Task.user_id == user_id,
            Task.status.in_(["TODO", "IN_PROGRESS"])
        ).order_by(
            priority_weight.desc(),
            Task.due_at.asc().nullslast(),
            Task.created_at.asc()
        ).limit(1)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
