from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.job import JobPosting, JobApplication, ApplicationEvent
from datetime import datetime, timezone

class JobRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_postings(self) -> List[JobPosting]:
        result = await self.db.execute(select(JobPosting).order_by(desc(JobPosting.created_at)))
        postings = list(result.scalars().all())
        if not postings:
            # Seed default postings
            defaults = [
                JobPosting(
                    title="Senior Backend Engineer (FastAPI/Python)",
                    company="Stripe",
                    location="Remote, US",
                    salary_range="$160,000 - $195,000",
                    description="Build hyper-scale financial transaction systems with Python, FastAPI, and Postgres.",
                    required_skills=[
                        {"name": "Python", "required_level": 80},
                        {"name": "FastAPI", "required_level": 75},
                        {"name": "SQL & PostgreSQL", "required_level": 75},
                        {"name": "System Architecture", "required_level": 70}
                    ]
                ),
                JobPosting(
                    title="Distributed Systems Engineer",
                    company="Datadog",
                    location="San Francisco, CA / Hybrid",
                    salary_range="$175,000 - $210,000",
                    description="Engineer real-time telemetry ingestion pipelines and microservice architectures.",
                    required_skills=[
                        {"name": "Python", "required_level": 70},
                        {"name": "Data Structures & Algorithms", "required_level": 80},
                        {"name": "AWS Cloud", "required_level": 75},
                        {"name": "Docker & Containers", "required_level": 70}
                    ]
                ),
                JobPosting(
                    title="Full Stack Engineer",
                    company="Linear",
                    location="Remote, Global",
                    salary_range="$150,000 - $185,000",
                    description="Design seamless product workflows across React, TypeScript, and high performance backend APIs.",
                    required_skills=[
                        {"name": "TypeScript", "required_level": 80},
                        {"name": "React", "required_level": 85},
                        {"name": "FastAPI", "required_level": 60}
                    ]
                )
            ]
            for p in defaults:
                self.db.add(p)
            await self.db.commit()
            return defaults
        return postings

    async def get_posting(self, job_id: UUID) -> Optional[JobPosting]:
        result = await self.db.execute(select(JobPosting).where(JobPosting.id == job_id))
        return result.scalar_one_or_none()

    async def list_applications(self, user_id: UUID) -> List[JobApplication]:
        result = await self.db.execute(
            select(JobApplication)
            .where(JobApplication.user_id == user_id)
            .order_by(desc(JobApplication.updated_at))
        )
        return list(result.scalars().all())

    async def get_application(self, app_id: UUID, user_id: UUID) -> Optional[JobApplication]:
        result = await self.db.execute(
            select(JobApplication)
            .where(JobApplication.id == app_id, JobApplication.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_application(self, user_id: UUID, job_id: UUID, status: str = "SAVED", notes: Optional[str] = None) -> JobApplication:
        app = JobApplication(user_id=user_id, job_id=job_id, status=status, notes=notes)
        self.db.add(app)
        await self.db.flush()
        
        event = ApplicationEvent(
            application_id=app.id,
            event_type="STATUS_CHANGE",
            title=f"Application initialized with status {status}"
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(app)
        return app

    async def update_status(self, app: JobApplication, new_status: str) -> JobApplication:
        app.status = new_status
        if new_status == "APPLIED" and not app.applied_at:
            app.applied_at = datetime.now(timezone.utc)
            
        event = ApplicationEvent(
            application_id=app.id,
            event_type="STATUS_CHANGE",
            title=f"Moved to {new_status}"
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(app)
        return app
