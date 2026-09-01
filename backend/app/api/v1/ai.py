from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ai_service import AIService
from app.schemas.ai import (
    AIConversationResponse, ChatRequest, ChatResponse, AIActionResponse
)

router = APIRouter()

@router.get("/conversations", response_model=List[AIConversationResponse])
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AIService(db)
    return await service.list_conversations(current_user.id)

@router.get("/conversations/{conversation_id}", response_model=AIConversationResponse)
async def get_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AIService(db)
    return await service.get_conversation(conversation_id, current_user.id)

@router.post("/chat", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AIService(db)
    return await service.chat(current_user.id, data)

@router.post("/actions/{action_id}/confirm", response_model=AIActionResponse)
async def confirm_action(
    action_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AIService(db)
    return await service.confirm_action(action_id, current_user.id)

@router.post("/actions/{action_id}/reject", response_model=AIActionResponse)
async def reject_action(
    action_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AIService(db)
    return await service.reject_action(action_id, current_user.id)
