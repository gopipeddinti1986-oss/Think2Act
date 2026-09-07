from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.job_repository import JobRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.activity_repository import ActivityRepository
from app.schemas.job import JobPostingResponse, JobApplicationResponse, JobApplicationCreate

class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.job_repo = JobRepository(db)
        self.skill_repo = SkillRepository(db)
        self.activity_repo = ActivityRepository(db)

    async def list_matched_jobs(self, user_id: UUID) -> List[JobPostingResponse]:
        postings = await self.job_repo.list_postings()
        user_skills = await self.skill_repo.list_user_skills(user_id)
        user_skill_map = {us.skill.name.lower(): float(us.level) for us in user_skills if us.skill}

        results: List[JobPostingResponse] = []
        for p in postings:
            reqs = p.required_skills or []
            if not reqs:
                results.append(JobPostingResponse.model_validate(p))
                continue

            matches = []
            missing = []
            for r in reqs:
                s_name = r.get("name", "")
                r_level = float(r.get("required_level", 50))
                u_level = user_skill_map.get(s_name.lower(), 0.0)
                
                ratio = min(1.0, u_level / r_level) if r_level > 0 else 1.0
                matches.append(ratio)
                if u_level < r_level:
                    missing.append(s_name)

            avg_match = round((sum(matches) / len(matches)) * 100, 1) if matches else 0.0
            resp = JobPostingResponse(
                id=p.id,
                title=p.title,
                company=p.company,
                location=p.location,
                salary_range=p.salary_range,
                description=p.description,
                required_skills=p.required_skills,
                match_percentage=avg_match,
                missing_skills=missing,
                created_at=p.created_at
            )
            results.append(resp)
        return results

    async def list_applications(self, user_id: UUID) -> List[JobApplicationResponse]:
        apps = await self.job_repo.list_applications(user_id)
        return [JobApplicationResponse.model_validate(a) for a in apps]

    async def create_application(self, user_id: UUID, data: JobApplicationCreate) -> JobApplicationResponse:
        job = await self.job_repo.get_posting(data.job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found.")
        app = await self.job_repo.create_application(user_id, data.job_id, data.status, data.notes)

        # Emit activity event
        await self.activity_repo.create_event(
            user_id=user_id,
            event_type="JOB_APPLICATION_CREATED",
            title=f"Application submitted for {job.title} at {job.company}",
            description=f"Status: {app.status}",
            entity_type="JOB_APPLICATION",
            entity_id=app.id,
            payload={"job_id": str(job.id), "status": app.status, "company": job.company, "title": job.title}
        )
        await self.db.commit()

        return JobApplicationResponse.model_validate(app)

    async def update_status(self, user_id: UUID, app_id: UUID, new_status: str) -> JobApplicationResponse:
        app = await self.job_repo.get_application(app_id, user_id)
        if not app:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found.")
        updated = await self.job_repo.update_status(app, new_status)

        job_title = updated.job.title if updated.job else "Role"
        company = updated.job.company if updated.job else "Company"

        # Emit activity event
        await self.activity_repo.create_event(
            user_id=user_id,
            event_type="JOB_APPLICATION_STATUS_UPDATED",
            title=f"Application status updated to {new_status} for {job_title}",
            description=f"Company: {company}",
            entity_type="JOB_APPLICATION",
            entity_id=updated.id,
            payload={"status": new_status, "job_id": str(updated.job_id)}
        )
        await self.db.commit()

        return JobApplicationResponse.model_validate(updated)
