from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.skill_service import SkillService
from app.schemas.skill import (
    SkillCreate, SkillResponse, UserSkillResponse, AssignTaskSkillsRequest
)

router = APIRouter()

@router.get("", response_model=List[SkillResponse])
async def list_global_skills(
    category: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    service = SkillService(db)
    return await service.list_skills(category)

@router.post("", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def create_skill_in_catalog(
    data: SkillCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = SkillService(db)
    return await service.create_skill(data)

@router.get("/me", response_model=List[UserSkillResponse])
async def get_my_skill_graph(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = SkillService(db)
    return await service.list_user_skills(current_user.id)

@router.get("/me/{skill_id}", response_model=UserSkillResponse)
async def get_my_skill_detail(
    skill_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = SkillService(db)
    return await service.get_user_skill(current_user.id, skill_id)

@router.post("/tasks/{task_id}/assign")
async def assign_skills_to_task(
    task_id: UUID,
    data: AssignTaskSkillsRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = SkillService(db)
    await service.skill_repo.assign_task_skills(task_id, data.skill_ids)
    return {"message": "Skills successfully linked to task."}
