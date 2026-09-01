from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate

class GoalRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, goal_id: UUID, user_id: UUID) -> Optional[Goal]:
        stmt = select(Goal).where(Goal.id == goal_id, Goal.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: UUID) -> List[Goal]:
        stmt = select(Goal).where(Goal.user_id == user_id).order_by(Goal.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, user_id: UUID, data: GoalCreate) -> Goal:
        goal = Goal(
            user_id=user_id,
            **data.model_dump()
        )
        self.db.add(goal)
        await self.db.commit()
        await self.db.refresh(goal)
        return goal

    async def update(self, goal_id: UUID, user_id: UUID, data: GoalUpdate) -> Optional[Goal]:
        goal = await self.get_by_id(goal_id, user_id)
        if not goal:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for key, val in update_data.items():
            setattr(goal, key, val)
        await self.db.commit()
        await self.db.refresh(goal)
        return goal

    async def delete(self, goal_id: UUID, user_id: UUID) -> bool:
        goal = await self.get_by_id(goal_id, user_id)
        if not goal:
            return False
        await self.db.delete(goal)
        await self.db.commit()
        return True
