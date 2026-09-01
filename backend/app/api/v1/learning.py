from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.learning_service import LearningService
from app.schemas.learning import (
    LearningResourceResponse, LearningPathResponse, LearningPathItemResponse,
    GenerateRoadmapRequest, ConvertLearningToTaskResponse, SkillGapReport
)

router = APIRouter()

@router.get("/resources", response_model=List[LearningResourceResponse])
async def list_learning_resources(
    db: AsyncSession = Depends(get_db)
):
    service = LearningService(db)
    return await service.list_learning_resources()

@router.get("/paths", response_model=List[LearningPathResponse])
async def list_user_learning_paths(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = LearningService(db)
    return await service.list_user_paths(current_user.id)

@router.post("/paths/generate", response_model=LearningPathResponse, status_code=status.HTTP_201_CREATED)
async def generate_learning_roadmap(
    data: GenerateRoadmapRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = LearningService(db)
    return await service.generate_learning_roadmap(current_user.id, data)

@router.post("/items/{item_id}/convert-to-task", response_model=ConvertLearningToTaskResponse)
async def convert_learning_item_to_task(
    item_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = LearningService(db)
    return await service.convert_item_to_task(item_id, current_user.id)

@router.post("/items/{item_id}/complete", response_model=LearningPathItemResponse)
async def complete_learning_item(
    item_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = LearningService(db)
    return await service.complete_path_item(item_id, current_user.id)
