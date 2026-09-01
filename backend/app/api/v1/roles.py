from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.learning_service import LearningService
from app.schemas.learning import RoleResponse

router = APIRouter()

@router.get("", response_model=List[RoleResponse])
async def list_roles(
    db: AsyncSession = Depends(get_db)
):
    service = LearningService(db)
    return await service.list_roles()
