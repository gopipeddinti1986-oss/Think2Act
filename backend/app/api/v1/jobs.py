from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.job import JobPostingResponse, JobApplicationResponse, JobApplicationCreate, JobApplicationUpdateStatus
from app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["Jobs & Applications"])

@router.get("", response_model=List[JobPostingResponse])
async def list_jobs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = JobService(db)
    return await service.list_matched_jobs(current_user.id)

@router.get("/applications", response_model=List[JobApplicationResponse])
async def list_applications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = JobService(db)
    return await service.list_applications(current_user.id)

@router.post("/applications", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    data: JobApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = JobService(db)
    return await service.create_application(current_user.id, data)

@router.patch("/applications/{app_id}/status", response_model=JobApplicationResponse)
async def update_application_status(
    app_id: UUID,
    data: JobApplicationUpdateStatus,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = JobService(db)
    return await service.update_status(current_user.id, app_id, data.status)
