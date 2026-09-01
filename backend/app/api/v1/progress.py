from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.productivity_service import ProductivityService
from app.schemas.productivity import ProductivityTrendResponse

router = APIRouter()

@router.get("/productivity", response_model=ProductivityTrendResponse)
async def get_productivity_trends(
    days: int = Query(30, ge=7, le=90),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ProductivityService(db)
    return await service.get_progress_trends(current_user.id, days=days)
