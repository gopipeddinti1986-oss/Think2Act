from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.resume import Resume, ResumeSuggestion

class ResumeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user(self, user_id: UUID) -> List[Resume]:
        result = await self.db.execute(
            select(Resume).where(Resume.user_id == user_id).order_by(desc(Resume.updated_at))
        )
        return list(result.scalars().all())

    async def get_by_id(self, resume_id: UUID, user_id: UUID) -> Optional[Resume]:
        result = await self.db.execute(
            select(Resume).where(Resume.id == resume_id, Resume.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: UUID, title: str, target_role: str, raw_text: Optional[str] = None) -> Resume:
        resume = Resume(
            user_id=user_id,
            title=title,
            target_role=target_role,
            raw_text=raw_text,
            ats_score=78.0,
            parsed_sections={
                "summary": "Experienced backend developer specialized in high concurrency microservices and scalable APIs.",
                "experience": [
                    "Engineered REST & GraphQL backend services handling 10k+ req/sec using FastAPI and PostgreSQL.",
                    "Implemented distributed Redis caching layer, decreasing p99 latency by 35%."
                ],
                "skills": ["Python", "FastAPI", "SQL", "PostgreSQL", "Docker", "AWS", "Redis"]
            }
        )
        self.db.add(resume)
        await self.db.flush()

        # Seed high-leverage ATS suggestions
        suggs = [
            ResumeSuggestion(
                resume_id=resume.id,
                section="experience",
                suggestion_type="QUANTIFIABLE_METRIC",
                current_text="Engineered REST & GraphQL backend services handling 10k+ req/sec using FastAPI and PostgreSQL.",
                recommended_text="Architected and deployed asynchronous FastAPI & PostgreSQL backend services handling 15k+ req/sec at sub-50ms p99 latency.",
                impact_reason="Adds exact performance benchmark and architectural leadership terminology for ATS scanners."
            ),
            ResumeSuggestion(
                resume_id=resume.id,
                section="skills",
                suggestion_type="MISSING_KEYWORD",
                current_text="Docker, AWS",
                recommended_text="Docker, Kubernetes, AWS (ECS, S3, RDS), CI/CD GitHub Actions",
                impact_reason="Aligns directly with Tier-1 Backend Engineer job listing keyword criteria."
            )
        ]
        for s in suggs:
            self.db.add(s)
        await self.db.commit()
        await self.db.refresh(resume)
        return resume

    async def apply_suggestion(self, resume_id: UUID, suggestion_id: UUID, user_id: UUID) -> Optional[Resume]:
        resume = await self.get_by_id(resume_id, user_id)
        if not resume:
            return None
        result = await self.db.execute(
            select(ResumeSuggestion).where(ResumeSuggestion.id == suggestion_id, ResumeSuggestion.resume_id == resume_id)
        )
        sugg = result.scalar_one_or_none()
        if sugg:
            sugg.is_applied = True
            resume.ats_score = min(100.0, resume.ats_score + 8.0)
            await self.db.commit()
            await self.db.refresh(resume)
        return resume
