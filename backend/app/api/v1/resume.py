from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.resume import ResumeResponse, ResumeCreate, ApplySuggestionRequest
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/resume", tags=["Resume & ATS"])

@router.get("", response_model=List[ResumeResponse])
async def list_resumes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.list_resumes(current_user.id)

@router.post("", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    data: ResumeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.create_resume(current_user.id, data)

@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.get_resume(current_user.id, resume_id)

@router.post("/{resume_id}/suggestions/{sugg_id}/apply", response_model=ResumeResponse)
async def apply_suggestion(
    resume_id: UUID,
    sugg_id: UUID,
    data: ApplySuggestionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.apply_suggestion(current_user.id, resume_id, sugg_id)
