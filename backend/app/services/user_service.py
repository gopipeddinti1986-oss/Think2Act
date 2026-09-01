from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserDetailResponse, UserProfileUpdate, UserProfileResponse

class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def get_current_user_profile(self, user: User) -> UserDetailResponse:
        full_user = await self.user_repo.get_by_id(user.id)
        if not full_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return UserDetailResponse.model_validate(full_user)

    async def update_profile(self, user: User, data: UserProfileUpdate) -> UserProfileResponse:
        profile = await self.user_repo.update_profile(user.id, **data.model_dump(exclude_unset=True))
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found.")
        return UserProfileResponse.model_validate(profile)
