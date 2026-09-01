from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.focus_service import FocusService
from app.schemas.focus import (
    FocusSessionStart, FocusSessionFinish, FocusSessionResponse, FocusSummaryToday
)

router = APIRouter()

@router.post("/sessions", response_model=FocusSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_focus_session(
    data: FocusSessionStart,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = FocusService(db)
    return await service.start_session(current_user.id, data)

@router.get("/active", response_model=Optional[FocusSessionResponse])
async def get_active_session(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = FocusService(db)
    return await service.get_active_session(current_user.id)

@router.post("/sessions/{session_id}/finish", response_model=FocusSessionResponse)
async def finish_focus_session(
    session_id: UUID,
    data: FocusSessionFinish,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = FocusService(db)
    return await service.finish_session(session_id, current_user.id, data)

@router.get("/sessions", response_model=List[FocusSessionResponse])
async def list_focus_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = FocusService(db)
    return await service.list_sessions(current_user.id)

@router.get("/today", response_model=FocusSummaryToday)
async def get_today_focus_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = FocusService(db)
    return await service.get_today_summary(current_user.id)
