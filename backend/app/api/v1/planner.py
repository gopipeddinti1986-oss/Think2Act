from typing import List, Optional
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.planner_service import PlannerService
from app.schemas.planner import (
    PlannerEntryCreate, PlannerEntryUpdate, PlannerEntryResponse,
    AutoScheduleResponse
)

router = APIRouter()

@router.get("", response_model=List[PlannerEntryResponse])
async def list_planner_entries(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = PlannerService(db)
    return await service.list_entries(current_user.id, start_time, end_time)

@router.post("", response_model=PlannerEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_planner_entry(
    data: PlannerEntryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = PlannerService(db)
    return await service.create_entry(current_user.id, data)

@router.patch("/{entry_id}", response_model=PlannerEntryResponse)
async def update_planner_entry(
    entry_id: UUID,
    data: PlannerEntryUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = PlannerService(db)
    return await service.update_entry(entry_id, current_user.id, data)

@router.delete("/{entry_id}")
async def delete_planner_entry(
    entry_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = PlannerService(db)
    return await service.delete_entry(entry_id, current_user.id)

@router.post("/auto-schedule", response_model=AutoScheduleResponse)
async def auto_schedule(
    schedule_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = PlannerService(db)
    target_date = schedule_date or datetime.now()
    return await service.auto_schedule_suggestions(current_user.id, target_date)
