from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse, Token, AuthUserResponse

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register(self, data: RegisterRequest) -> AuthResponse:
        existing_user = await self.user_repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists."
            )
        hashed_pwd = get_password_hash(data.password)
        user = await self.user_repo.create(
            name=data.name,
            email=data.email,
            password_hash=hashed_pwd
        )
        token_str = create_access_token(user.id)
        return AuthResponse(
            user=AuthUserResponse.model_validate(user),
            token=Token(access_token=token_str)
        )

    async def login(self, data: LoginRequest) -> AuthResponse:
        user = await self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive."
            )
        token_str = create_access_token(user.id)
        return AuthResponse(
            user=AuthUserResponse.model_validate(user),
            token=Token(access_token=token_str)
        )
