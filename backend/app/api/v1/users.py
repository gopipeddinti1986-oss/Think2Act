from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.user_service import UserService
from app.services.activity_service import ActivityService
from app.schemas.user import UserDetailResponse, UserProfileUpdate, UserProfileResponse
from app.schemas.activity import ActivityEventResponse

router = APIRouter()

@router.get("/me", response_model=UserDetailResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    return await service.get_current_user_profile(current_user)

@router.patch("/me", response_model=UserProfileResponse)
async def update_user_profile(
    data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    return await service.update_profile(current_user, data)

@router.get("/activity", response_model=List[ActivityEventResponse])
async def get_user_activity(
    limit: int = 20,
    event_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ActivityService(db)
    return await service.get_recent_activities(current_user.id, limit=limit, event_type=event_type)
