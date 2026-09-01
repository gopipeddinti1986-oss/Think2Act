from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.ai_repository import AIRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.planner_repository import PlannerRepository
from app.ai.orchestrator import AIOrchestrator
from app.schemas.ai import (
    AIConversationResponse, AIMessageResponse, AIActionResponse,
    ChatRequest, ChatResponse
)
from app.schemas.task import TaskCreate
from app.schemas.planner import PlannerEntryCreate

class AIService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai_repo = AIRepository(db)
        self.task_repo = TaskRepository(db)
        self.planner_repo = PlannerRepository(db)
        self.orchestrator = AIOrchestrator(db)

    async def list_conversations(self, user_id: UUID) -> List[AIConversationResponse]:
        convs = await self.ai_repo.list_conversations(user_id)
        return [AIConversationResponse.model_validate(c) for c in convs]

    async def get_conversation(self, conversation_id: UUID, user_id: UUID) -> AIConversationResponse:
        conv = await self.ai_repo.get_conversation(conversation_id, user_id)
        if not conv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")
        return AIConversationResponse.model_validate(conv)

    async def chat(self, user_id: UUID, data: ChatRequest) -> ChatResponse:
        # 1. Get or create conversation
        if data.conversation_id:
            conv = await self.ai_repo.get_conversation(data.conversation_id, user_id)
            if not conv:
                conv = await self.ai_repo.create_conversation(user_id, title=data.message[:30])
        else:
            conv = await self.ai_repo.create_conversation(user_id, title=data.message[:30])

        # 2. Record User Message
        await self.ai_repo.add_message(conv.id, role="user", content=data.message)

        # 3. Run AI Orchestrator Reasoning
        result = await self.orchestrator.process_user_message(user_id, data.message)

        # 4. Record Assistant Message
        assistant_msg = await self.ai_repo.add_message(conv.id, role="assistant", content=result["response_text"])

        # 5. Record Proposed Actions as PENDING
        saved_actions: List[AIActionResponse] = []
        for prop in result["proposed_actions"]:
            action = await self.ai_repo.create_action(
                user_id=user_id,
                conversation_id=conv.id,
                action_type=prop["action_type"],
                target_type=prop["target_type"],
                target_id=prop.get("target_id"),
                payload=prop.get("payload"),
                requires_confirmation=prop.get("requires_confirmation", True)
            )
            saved_actions.append(AIActionResponse.model_validate(action))

        return ChatResponse(
            conversation_id=conv.id,
            message=AIMessageResponse.model_validate(assistant_msg),
            proposed_actions=saved_actions
        )

    async def confirm_action(self, action_id: UUID, user_id: UUID) -> AIActionResponse:
        action = await self.ai_repo.get_action(action_id, user_id)
        if not action:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI Action proposal not found.")
        if action.status != "PENDING":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Action is already {action.status}.")

        payload = action.payload or {}

        # Execute based on action_type
        if action.action_type == "CREATE_TASK":
            await self.task_repo.create(
                user_id=user_id,
                data=TaskCreate(
                    title=payload.get("title", "AI Task"),
                    description=payload.get("description"),
                    priority=payload.get("priority", "MEDIUM"),
                    estimated_minutes=payload.get("estimated_minutes", 45),
                    category=payload.get("category", "General"),
                    status="TODO"
                )
            )

        elif action.action_type == "SCHEDULE_TASK":
            await self.planner_repo.create(
                user_id=user_id,
                data=PlannerEntryCreate(
                    task_id=UUID(payload["task_id"]),
                    start_at=datetime.fromisoformat(payload["start_at"]),
                    end_at=datetime.fromisoformat(payload["end_at"]),
                    status="SCHEDULED",
                    source="AI_COACH"
                )
            )

        elif action.action_type == "COMPLETE_TASK":
            task_id = action.target_id or UUID(payload["task_id"])
            await self.task_repo.complete(task_id, user_id)

        action.status = "EXECUTED"
        action.confirmed_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(action)
        return AIActionResponse.model_validate(action)

    async def reject_action(self, action_id: UUID, user_id: UUID) -> AIActionResponse:
        action = await self.ai_repo.get_action(action_id, user_id)
        if not action:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI Action proposal not found.")
        action.status = "REJECTED"
        await self.db.commit()
        await self.db.refresh(action)
        return AIActionResponse.model_validate(action)
