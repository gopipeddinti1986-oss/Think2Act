from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.decision_repository import DecisionRepository
from app.schemas.decision import DecisionResponse, DecisionCreate, UpdateOptionScoreRequest

class DecisionService:
    def __init__(self, db: AsyncSession):
        self.decision_repo = DecisionRepository(db)

    async def list_decisions(self, user_id: UUID) -> List[DecisionResponse]:
        decisions = await self.decision_repo.list_by_user(user_id)
        if not decisions:
            init_d = await self.decision_repo.create(
                user_id=user_id,
                title="Career Path Strategy: Startup vs High-Scale SaaS",
                description="Comparative multi-factor evaluation of offer leverage, growth velocity, and architectural learning."
            )
            return [DecisionResponse.model_validate(init_d)]
        return [DecisionResponse.model_validate(d) for d in decisions]

    async def create_decision(self, user_id: UUID, data: DecisionCreate) -> DecisionResponse:
        decision = await self.decision_repo.create(
            user_id=user_id,
            title=data.title,
            description=data.description,
            category=data.category,
            options=data.options,
            criteria=data.criteria
        )
        return DecisionResponse.model_validate(decision)

    async def get_decision(self, user_id: UUID, decision_id: UUID) -> DecisionResponse:
        decision = await self.decision_repo.get_by_id(decision_id, user_id)
        if not decision:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Decision not found.")
        return DecisionResponse.model_validate(decision)

    async def update_score(self, user_id: UUID, decision_id: UUID, data: UpdateOptionScoreRequest) -> DecisionResponse:
        decision = await self.decision_repo.get_by_id(decision_id, user_id)
        if not decision:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Decision not found.")
        
        updated = await self.decision_repo.update_score(
            decision_id=decision_id,
            option_id=data.option_id,
            criterion_id=data.criterion_id,
            score=data.score,
            rationale=data.rationale
        )
        return DecisionResponse.model_validate(updated)
