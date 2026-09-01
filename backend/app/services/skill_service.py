from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.skill_repository import SkillRepository
from app.repositories.evidence_repository import EvidenceRepository
from app.schemas.skill import (
    SkillCreate, SkillResponse, UserSkillResponse, EvidenceItemResponse,
    SkillHistoryPoint
)
from app.schemas.evidence import EvidenceCreate, EvidenceResponse

DEFAULT_SKILL_SEEDS = [
    {"name": "Python", "category": "Programming", "description": "Core Python programming, OOP, data structures"},
    {"name": "FastAPI", "category": "Backend", "description": "High-performance Python web APIs and dependency injection"},
    {"name": "SQL & PostgreSQL", "category": "Database", "description": "Relational schemas, queries, joins, indexes, transactions"},
    {"name": "Data Structures & Algorithms", "category": "DSA", "description": "Trees, Graphs, Dynamic Programming, Complexity analysis"},
    {"name": "Docker & Containers", "category": "Cloud & DevOps", "description": "Containerization, multi-stage builds, Docker Compose"},
    {"name": "React & TypeScript", "category": "Frontend", "description": "Component architecture, hooks, modern state management"},
    {"name": "Git & Version Control", "category": "DevOps", "description": "Branching, PRs, merge strategies, Git workflows"},
    {"name": "AWS Cloud", "category": "Cloud & DevOps", "description": "Cloud deployment, EC2, S3, IAM, Serverless architecture"},
]

class SkillService:
    def __init__(self, db: AsyncSession):
        self.skill_repo = SkillRepository(db)
        self.evidence_repo = EvidenceRepository(db)

    async def ensure_default_seeds(self):
        for seed in DEFAULT_SKILL_SEEDS:
            existing = await self.skill_repo.get_by_name(seed["name"])
            if not existing:
                await self.skill_repo.create(
                    name=seed["name"],
                    category=seed["category"],
                    description=seed["description"]
                )

    async def list_skills(self, category: Optional[str] = None) -> List[SkillResponse]:
        await self.ensure_default_seeds()
        skills = await self.skill_repo.list_all(category)
        return [SkillResponse.model_validate(s) for s in skills]

    async def create_skill(self, data: SkillCreate) -> SkillResponse:
        existing = await self.skill_repo.get_by_name(data.name)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Skill already exists.")
        skill = await self.skill_repo.create(data.name, data.category, data.description)
        return SkillResponse.model_validate(skill)

    async def list_user_skills(self, user_id: UUID) -> List[UserSkillResponse]:
        await self.ensure_default_seeds()
        user_skills = await self.skill_repo.list_user_skills(user_id)
        
        # If user has no skills initialized yet, create initial default user_skill links with baseline evidence
        if not user_skills:
            all_skills = await self.skill_repo.list_all()
            for s in all_skills[:5]:
                await self.skill_repo.update_user_skill_level(
                    user_id=user_id,
                    skill_id=s.id,
                    level=30.0,
                    confidence=0.4,
                    reason="Initial profile setup"
                )
            user_skills = await self.skill_repo.list_user_skills(user_id)

        responses: List[UserSkillResponse] = []
        for us in user_skills:
            evidence_items = await self.evidence_repo.list_by_user_and_skill(user_id, us.skill_id)
            history_items = await self.skill_repo.get_skill_history(user_id, us.skill_id)
            
            responses.append(UserSkillResponse(
                skill_id=us.skill_id,
                name=us.skill.name,
                category=us.skill.category,
                level=float(us.level),
                confidence=float(us.confidence),
                last_assessed_at=us.last_assessed_at,
                evidence_count=len(evidence_items),
                recent_evidence=[EvidenceItemResponse.model_validate(e) for e in evidence_items[:5]],
                history=[SkillHistoryPoint.model_validate(h) for h in history_items[:10]]
            ))
        return responses

    async def get_user_skill(self, user_id: UUID, skill_id: UUID) -> UserSkillResponse:
        user_skill = await self.skill_repo.get_user_skill(user_id, skill_id)
        if not user_skill:
            skill = await self.skill_repo.get_by_id(skill_id)
            if not skill:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found.")
            user_skill = await self.skill_repo.update_user_skill_level(user_id, skill_id, 0.0, 0.3)

        evidence_items = await self.evidence_repo.list_by_user_and_skill(user_id, skill_id)
        history_items = await self.skill_repo.get_skill_history(user_id, skill_id)

        return UserSkillResponse(
            skill_id=user_skill.skill_id,
            name=user_skill.skill.name,
            category=user_skill.skill.category,
            level=float(user_skill.level),
            confidence=float(user_skill.confidence),
            last_assessed_at=user_skill.last_assessed_at,
            evidence_count=len(evidence_items),
            recent_evidence=[EvidenceItemResponse.model_validate(e) for e in evidence_items],
            history=[SkillHistoryPoint.model_validate(h) for h in history_items]
        )

    async def add_evidence_and_recalculate(
        self,
        user_id: UUID,
        data: EvidenceCreate
    ) -> EvidenceResponse:
        skill = await self.skill_repo.get_by_id(data.skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found.")

        # 1. Record evidence
        evidence = await self.evidence_repo.create(
            user_id=user_id,
            skill_id=data.skill_id,
            source_type=data.source_type,
            description=data.description,
            strength=data.strength,
            source_id=data.source_id
        )

        # 2. Evidence-based scoring engine
        # Total strength + source diversity formula:
        evidence_items = await self.evidence_repo.list_by_user_and_skill(user_id, data.skill_id)
        total_strength = sum(float(e.strength) for e in evidence_items)
        unique_sources = len(set(e.source_type for e in evidence_items))

        # Level: progressive curve up to 100
        computed_level = min(100.0, round(15.0 + (total_strength * 0.85), 1))
        
        # Confidence: scales with evidence count and diverse sources
        computed_confidence = min(0.95, round(0.4 + (len(evidence_items) * 0.1) + (unique_sources * 0.05), 2))

        # 3. Update UserSkill and record history point
        await self.skill_repo.update_user_skill_level(
            user_id=user_id,
            skill_id=data.skill_id,
            level=computed_level,
            confidence=computed_confidence,
            reason=f"New evidence added: {data.description[:60]}"
        )

        return EvidenceResponse.model_validate(evidence)

    async def on_task_completed(self, user_id: UUID, task_id: UUID, task_title: str):
        # Find skills associated with task
        task_skills = await self.skill_repo.get_task_skills(task_id)
        for skill in task_skills:
            await self.add_evidence_and_recalculate(
                user_id=user_id,
                data=EvidenceCreate(
                    skill_id=skill.id,
                    source_type="TASK_EXECUTION",
                    source_id=task_id,
                    strength=12.5,
                    description=f"Successfully completed task: {task_title}"
                )
            )
