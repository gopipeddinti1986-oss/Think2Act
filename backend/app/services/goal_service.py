from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.goal_repository import GoalRepository
from app.repositories.activity_repository import ActivityRepository
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse

class GoalService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = GoalRepository(db)
        self.activity_repo = ActivityRepository(db)

    async def list_goals(self, user_id: UUID) -> List[GoalResponse]:
        goals = await self.repo.list_by_user(user_id)
        return [
            GoalResponse(
                id=g.id,
                user_id=g.user_id,
                title=g.title,
                description=g.description,
                category=g.category,
                priority=g.priority,
                status=g.status,
                start_date=g.start_date,
                target_date=g.target_date,
                calculated_progress=g.calculated_progress,
                health=g.health,
                created_at=g.created_at,
                updated_at=g.updated_at
            )
            for g in goals
        ]

    async def get_goal(self, goal_id: UUID, user_id: UUID) -> GoalResponse:
        goal = await self.repo.get_by_id(goal_id, user_id)
        if not goal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found.")
        return GoalResponse(
            id=goal.id,
            user_id=goal.user_id,
            title=goal.title,
            description=goal.description,
            category=goal.category,
            priority=goal.priority,
            status=goal.status,
            start_date=goal.start_date,
            target_date=goal.target_date,
            calculated_progress=goal.calculated_progress,
            health=goal.health,
            created_at=goal.created_at,
            updated_at=goal.updated_at
        )

    async def create_goal(self, user_id: UUID, data: GoalCreate) -> GoalResponse:
        goal = await self.repo.create(user_id, data)
        await self.activity_repo.create(
            user_id=user_id,
            event_type="GOAL_CREATED",
            title=f"Created Goal: {goal.title}",
            description=goal.description,
            entity_type="goal",
            entity_id=goal.id,
            payload={"category": goal.category, "priority": goal.priority}
        )
        return GoalResponse(
            id=goal.id,
            user_id=goal.user_id,
            title=goal.title,
            description=goal.description,
            category=goal.category,
            priority=goal.priority,
            status=goal.status,
            start_date=goal.start_date,
            target_date=goal.target_date,
            calculated_progress=goal.calculated_progress,
            health=goal.health,
            created_at=goal.created_at,
            updated_at=goal.updated_at
        )

    async def update_goal(self, goal_id: UUID, user_id: UUID, data: GoalUpdate) -> GoalResponse:
        goal = await self.repo.update(goal_id, user_id, data)
        if not goal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found.")
        return GoalResponse(
            id=goal.id,
            user_id=goal.user_id,
            title=goal.title,
            description=goal.description,
            category=goal.category,
            priority=goal.priority,
            status=goal.status,
            start_date=goal.start_date,
            target_date=goal.target_date,
            calculated_progress=goal.calculated_progress,
            health=goal.health,
            created_at=goal.created_at,
            updated_at=goal.updated_at
        )

    async def delete_goal(self, goal_id: UUID, user_id: UUID) -> dict:
        success = await self.repo.delete(goal_id, user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found.")
        return {"message": "Goal deleted successfully."}
