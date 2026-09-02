from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.decision import DecisionResponse, DecisionCreate, UpdateOptionScoreRequest
from app.services.decision_service import DecisionService

router = APIRouter(prefix="/decisions", tags=["Decision Simulator"])

@router.get("", response_model=List[DecisionResponse])
async def list_decisions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DecisionService(db)
    return await service.list_decisions(current_user.id)

@router.post("", response_model=DecisionResponse, status_code=status.HTTP_201_CREATED)
async def create_decision(
    data: DecisionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DecisionService(db)
    return await service.create_decision(current_user.id, data)

@router.get("/{decision_id}", response_model=DecisionResponse)
async def get_decision(
    decision_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DecisionService(db)
    return await service.get_decision(current_user.id, decision_id)

@router.post("/{decision_id}/score", response_model=DecisionResponse)
async def update_decision_score(
    decision_id: UUID,
    data: UpdateOptionScoreRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DecisionService(db)
    return await service.update_score(current_user.id, decision_id, data)
