from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.interview import InterviewSessionResponse, InterviewSessionCreate, SubmitAnswerRequest, InterviewQuestionResponse
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/interviews", tags=["Interview Intelligence"])

@router.get("", response_model=List[InterviewSessionResponse])
async def list_interview_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewService(db)
    return await service.list_sessions(current_user.id)

@router.post("", response_model=InterviewSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_interview_session(
    data: InterviewSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewService(db)
    return await service.start_session(current_user.id, data)

@router.get("/{session_id}", response_model=InterviewSessionResponse)
async def get_interview_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewService(db)
    return await service.get_session(current_user.id, session_id)

@router.post("/{session_id}/answer", response_model=InterviewQuestionResponse)
async def submit_question_answer(
    session_id: UUID,
    data: SubmitAnswerRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewService(db)
    return await service.submit_answer(current_user.id, session_id, data)
