from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.skill_service import SkillService
from app.schemas.evidence import EvidenceCreate, EvidenceResponse

router = APIRouter()

@router.get("", response_model=List[EvidenceResponse])
async def list_my_evidence(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = SkillService(db)
    items = await service.evidence_repo.list_by_user(current_user.id)
    return [EvidenceResponse.model_validate(e) for e in items]

@router.post("/manual", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
async def add_manual_evidence(
    data: EvidenceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = SkillService(db)
    return await service.add_evidence_and_recalculate(current_user.id, data)
