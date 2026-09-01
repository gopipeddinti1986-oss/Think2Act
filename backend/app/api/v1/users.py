from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.user_service import UserService
from app.schemas.user import UserDetailResponse, UserProfileUpdate, UserProfileResponse

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
