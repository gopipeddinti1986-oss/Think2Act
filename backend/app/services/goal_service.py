from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.goal_repository import GoalRepository
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse

class GoalService:
    def __init__(self, db: AsyncSession):
        self.repo = GoalRepository(db)

    async def list_goals(self, user_id: UUID) -> List[GoalResponse]:
        goals = await self.repo.list_by_user(user_id)
        return [GoalResponse.model_validate(g) for g in goals]

    async def get_goal(self, goal_id: UUID, user_id: UUID) -> GoalResponse:
        goal = await self.repo.get_by_id(goal_id, user_id)
        if not goal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found.")
        return GoalResponse.model_validate(goal)

    async def create_goal(self, user_id: UUID, data: GoalCreate) -> GoalResponse:
        goal = await self.repo.create(user_id, data)
        return GoalResponse.model_validate(goal)

    async def update_goal(self, goal_id: UUID, user_id: UUID, data: GoalUpdate) -> GoalResponse:
        goal = await self.repo.update(goal_id, user_id, data)
        if not goal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found.")
        return GoalResponse.model_validate(goal)

    async def delete_goal(self, goal_id: UUID, user_id: UUID) -> dict:
        success = await self.repo.delete(goal_id, user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found.")
        return {"message": "Goal deleted successfully."}
