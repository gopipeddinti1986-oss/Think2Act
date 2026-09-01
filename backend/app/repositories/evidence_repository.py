from typing import Optional, List
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models.skill import Evidence

class EvidenceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user_and_skill(self, user_id: UUID, skill_id: UUID) -> List[Evidence]:
        stmt = (
            select(Evidence)
            .where(Evidence.user_id == user_id, Evidence.skill_id == skill_id)
            .order_by(Evidence.occurred_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_by_user(self, user_id: UUID, limit: int = 50) -> List[Evidence]:
        stmt = (
            select(Evidence)
            .options(selectinload(Evidence.skill))
            .where(Evidence.user_id == user_id)
            .order_by(Evidence.occurred_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(
        self,
        user_id: UUID,
        skill_id: UUID,
        source_type: str,
        description: str,
        strength: float = 10.0,
        source_id: Optional[UUID] = None
    ) -> Evidence:
        evidence = Evidence(
            user_id=user_id,
            skill_id=skill_id,
            source_type=source_type,
            source_id=source_id,
            strength=strength,
            description=description
        )
        self.db.add(evidence)
        await self.db.commit()
        await self.db.refresh(evidence)
        return evidence

    async def get_total_strength_and_count(self, user_id: UUID, skill_id: UUID):
        stmt = select(
            func.count(Evidence.id),
            func.coalesce(func.sum(Evidence.strength), 0)
        ).where(Evidence.user_id == user_id, Evidence.skill_id == skill_id)
        result = await self.db.execute(stmt)
        count, total_strength = result.first()
        return count, float(total_strength)
