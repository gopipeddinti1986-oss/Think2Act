from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.repositories.activity_repository import ActivityRepository
from app.core.security import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token, decode_token
)
from app.schemas.auth import (
    RegisterRequest, LoginRequest, AuthResponse, Token,
    AuthUserResponse, RefreshTokenRequest
)

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.activity_repo = ActivityRepository(db)

    async def register(self, data: RegisterRequest) -> AuthResponse:
        existing_user = await self.user_repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists."
            )
        hashed_pwd = get_password_hash(data.password)
        try:
            user = await self.user_repo.create(
                name=data.name,
                email=data.email,
                password_hash=hashed_pwd,
                commit=False
            )
            access_tok = create_access_token(user.id)
            refresh_tok = create_refresh_token(user.id)

            # Log Activity Event
            await self.activity_repo.create(
                user_id=user.id,
                event_type="USER_REGISTERED",
                title="Account created",
                description=f"Welcome {user.name} to Think2Act."
            )

            await self.db.commit()
            await self.db.refresh(user, ["profile"])
        except Exception:
            await self.db.rollback()
            raise

        return AuthResponse(
            user=AuthUserResponse.model_validate(user),
            token=Token(access_token=access_tok, refresh_token=refresh_tok)
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
        access_tok = create_access_token(user.id)
        refresh_tok = create_refresh_token(user.id)

        # Log Activity Event
        try:
            await self.activity_repo.create(
                user_id=user.id,
                event_type="USER_LOGGED_IN",
                title="Session started",
                description="Signed into Think2Act workspace."
            )
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            # Do not fail login if activity logging fails, but log rollback

        return AuthResponse(
            user=AuthUserResponse.model_validate(user),
            token=Token(access_token=access_tok, refresh_token=refresh_tok)
        )

    async def refresh_token(self, data: RefreshTokenRequest) -> AuthResponse:
        payload = decode_token(data.refresh_token, expected_type="refresh")
        if not payload or not payload.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token."
            )
        try:
            user_id = UUID(payload["sub"])
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Malformed token subject."
            )
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account not found or inactive."
            )
        new_access = create_access_token(user.id)
        new_refresh = create_refresh_token(user.id)

        return AuthResponse(
            user=AuthUserResponse.model_validate(user),
            token=Token(access_token=new_access, refresh_token=new_refresh)
        )
