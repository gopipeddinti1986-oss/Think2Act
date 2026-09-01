from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.models.ai import AIConversation, AIMessage, AIAction

class AIRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_conversations(self, user_id: UUID) -> List[AIConversation]:
        stmt = (
            select(AIConversation)
            .where(AIConversation.user_id == user_id)
            .order_by(AIConversation.updated_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_conversation(self, conversation_id: UUID, user_id: UUID) -> Optional[AIConversation]:
        stmt = (
            select(AIConversation)
            .options(
                selectinload(AIConversation.messages),
                selectinload(AIConversation.actions)
            )
            .where(AIConversation.id == conversation_id, AIConversation.user_id == user_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_conversation(self, user_id: UUID, title: str = "New Coaching Session") -> AIConversation:
        conv = AIConversation(user_id=user_id, title=title)
        self.db.add(conv)
        await self.db.commit()
        await self.db.refresh(conv)
        return conv

    async def add_message(self, conversation_id: UUID, role: str, content: str) -> AIMessage:
        msg = AIMessage(conversation_id=conversation_id, role=role, content=content)
        self.db.add(msg)
        await self.db.commit()
        await self.db.refresh(msg)
        return msg

    async def create_action(
        self,
        user_id: UUID,
        conversation_id: Optional[UUID],
        action_type: str,
        target_type: str,
        target_id: Optional[UUID] = None,
        payload: Optional[Dict[str, Any]] = None,
        requires_confirmation: bool = True
    ) -> AIAction:
        action = AIAction(
            user_id=user_id,
            conversation_id=conversation_id,
            action_type=action_type,
            target_type=target_type,
            target_id=target_id,
            payload=payload,
            status="PENDING",
            requires_confirmation=requires_confirmation
        )
        self.db.add(action)
        await self.db.commit()
        await self.db.refresh(action)
        return action

    async def get_action(self, action_id: UUID, user_id: UUID) -> Optional[AIAction]:
        stmt = select(AIAction).where(AIAction.id == action_id, AIAction.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
