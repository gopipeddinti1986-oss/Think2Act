from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse, AuthUserResponse

router = APIRouter()

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.register(data)

@router.post("/login", response_model=AuthResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.login(data)

@router.get("/me", response_model=AuthUserResponse)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    return AuthUserResponse.model_validate(current_user)

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    return {"message": "Successfully logged out."}
