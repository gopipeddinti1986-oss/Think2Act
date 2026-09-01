from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from app.models.learning import (
    Role, RoleSkill, LearningResource, LearningResourceSkill,
    LearningPath, LearningPathItem
)
from app.models.skill import Skill

class LearningRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_role_by_id(self, role_id: UUID) -> Optional[Role]:
        stmt = (
            select(Role)
            .options(selectinload(Role.role_skills).selectinload(RoleSkill.skill))
            .where(Role.id == role_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_role_by_name(self, name: str) -> Optional[Role]:
        stmt = (
            select(Role)
            .options(selectinload(Role.role_skills).selectinload(RoleSkill.skill))
            .where(func.lower(Role.name) == name.lower().strip())
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_roles(self) -> List[Role]:
        stmt = (
            select(Role)
            .options(selectinload(Role.role_skills).selectinload(RoleSkill.skill))
            .order_by(Role.name.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_role(self, name: str, category: Optional[str] = None, description: Optional[str] = None) -> Role:
        role = Role(name=name.strip(), category=category, description=description)
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role

    async def add_role_skill(self, role_id: UUID, skill_id: UUID, required_level: float, importance: str = "HIGH"):
        rs = RoleSkill(role_id=role_id, skill_id=skill_id, required_level=required_level, importance=importance)
        self.db.add(rs)
        await self.db.commit()

    async def list_resources(self) -> List[LearningResource]:
        stmt = select(LearningResource).options(selectinload(LearningResource.skills)).order_by(LearningResource.title.asc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_resource(
        self,
        title: str,
        provider: Optional[str] = None,
        url: Optional[str] = None,
        description: Optional[str] = None,
        difficulty: str = "Intermediate"
    ) -> LearningResource:
        res = LearningResource(
            title=title,
            provider=provider,
            url=url,
            description=description,
            difficulty=difficulty
        )
        self.db.add(res)
        await self.db.commit()
        await self.db.refresh(res)
        return res

    async def link_resource_skill(self, resource_id: UUID, skill_id: UUID):
        lrs = LearningResourceSkill(resource_id=resource_id, skill_id=skill_id)
        self.db.add(lrs)
        await self.db.commit()

    async def list_paths_by_user(self, user_id: UUID) -> List[LearningPath]:
        stmt = (
            select(LearningPath)
            .options(
                selectinload(LearningPath.items).selectinload(LearningPathItem.skill),
                selectinload(LearningPath.items).selectinload(LearningPathItem.resource),
            )
            .where(LearningPath.user_id == user_id)
            .order_by(LearningPath.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_path_by_id(self, path_id: UUID, user_id: UUID) -> Optional[LearningPath]:
        stmt = (
            select(LearningPath)
            .options(
                selectinload(LearningPath.items).selectinload(LearningPathItem.skill),
                selectinload(LearningPath.items).selectinload(LearningPathItem.resource),
            )
            .where(LearningPath.id == path_id, LearningPath.user_id == user_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_path(
        self,
        user_id: UUID,
        title: str,
        role_id: Optional[UUID] = None,
        goal_id: Optional[UUID] = None
    ) -> LearningPath:
        path = LearningPath(
            user_id=user_id,
            title=title,
            role_id=role_id,
            goal_id=goal_id,
            status="ACTIVE"
        )
        self.db.add(path)
        await self.db.commit()
        await self.db.refresh(path)
        return path

    async def add_path_item(
        self,
        learning_path_id: UUID,
        skill_id: UUID,
        title: str,
        sequence_number: int,
        resource_id: Optional[UUID] = None
    ) -> LearningPathItem:
        item = LearningPathItem(
            learning_path_id=learning_path_id,
            skill_id=skill_id,
            title=title,
            sequence_number=sequence_number,
            resource_id=resource_id,
            status="PENDING",
            progress=0.0
        )
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def get_path_item_by_id(self, item_id: UUID) -> Optional[LearningPathItem]:
        stmt = (
            select(LearningPathItem)
            .options(
                selectinload(LearningPathItem.learning_path),
                selectinload(LearningPathItem.skill),
                selectinload(LearningPathItem.resource),
            )
            .where(LearningPathItem.id == item_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
