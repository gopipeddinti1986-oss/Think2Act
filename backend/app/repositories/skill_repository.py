from typing import Optional, List, Tuple
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from app.models.skill import Skill, UserSkill, Evidence, SkillHistory, TaskSkill

class SkillRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, skill_id: UUID) -> Optional[Skill]:
        stmt = select(Skill).where(Skill.id == skill_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Skill]:
        stmt = select(Skill).where(func.lower(Skill.name) == name.lower().strip())
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self, category: Optional[str] = None) -> List[Skill]:
        stmt = select(Skill)
        if category:
            stmt = stmt.where(Skill.category == category)
        stmt = stmt.order_by(Skill.name.asc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, name: str, category: Optional[str] = None, description: Optional[str] = None) -> Skill:
        skill = Skill(
            name=name.strip(),
            category=category,
            description=description
        )
        self.db.add(skill)
        await self.db.commit()
        await self.db.refresh(skill)
        return skill

    async def get_user_skill(self, user_id: UUID, skill_id: UUID) -> Optional[UserSkill]:
        stmt = (
            select(UserSkill)
            .options(selectinload(UserSkill.skill))
            .where(UserSkill.user_id == user_id, UserSkill.skill_id == skill_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_user_skills(self, user_id: UUID) -> List[UserSkill]:
        stmt = (
            select(UserSkill)
            .options(selectinload(UserSkill.skill))
            .where(UserSkill.user_id == user_id)
            .order_by(UserSkill.level.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update_user_skill_level(
        self,
        user_id: UUID,
        skill_id: UUID,
        level: float,
        confidence: float,
        reason: Optional[str] = None
    ) -> UserSkill:
        user_skill = await self.get_user_skill(user_id, skill_id)
        now = datetime.now(timezone.utc)
        if not user_skill:
            user_skill = UserSkill(
                user_id=user_id,
                skill_id=skill_id,
                level=level,
                confidence=confidence,
                last_assessed_at=now
            )
            self.db.add(user_skill)
        else:
            user_skill.level = level
            user_skill.confidence = confidence
            user_skill.last_assessed_at = now

        # Add history point
        history = SkillHistory(
            user_id=user_id,
            skill_id=skill_id,
            level=level,
            confidence=confidence,
            reason=reason or "Evidence evaluation update",
            recorded_at=now
        )
        self.db.add(history)

        await self.db.commit()
        await self.db.refresh(user_skill, ["skill"])
        return user_skill

    async def get_skill_history(self, user_id: UUID, skill_id: UUID, limit: int = 10) -> List[SkillHistory]:
        stmt = (
            select(SkillHistory)
            .where(SkillHistory.user_id == user_id, SkillHistory.skill_id == skill_id)
            .order_by(SkillHistory.recorded_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def assign_task_skills(self, task_id: UUID, skill_ids: List[UUID]):
        for sid in skill_ids:
            # check exists
            stmt = select(TaskSkill).where(TaskSkill.task_id == task_id, TaskSkill.skill_id == sid)
            res = await self.db.execute(stmt)
            if not res.scalar_one_or_none():
                ts = TaskSkill(task_id=task_id, skill_id=sid)
                self.db.add(ts)
        await self.db.commit()

    async def get_task_skills(self, task_id: UUID) -> List[Skill]:
        stmt = (
            select(Skill)
            .join(TaskSkill, TaskSkill.skill_id == Skill.id)
            .where(TaskSkill.task_id == task_id)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
