from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.resume_repository import ResumeRepository
from app.schemas.resume import ResumeResponse, ResumeCreate

class ResumeService:
    def __init__(self, db: AsyncSession):
        self.resume_repo = ResumeRepository(db)

    async def list_resumes(self, user_id: UUID) -> List[ResumeResponse]:
        resumes = await self.resume_repo.list_by_user(user_id)
        if not resumes:
            # Auto-create initial resume profile
            init_r = await self.resume_repo.create(
                user_id=user_id,
                title="Master Technical Resume",
                target_role="Backend Software Engineer"
            )
            return [ResumeResponse.model_validate(init_r)]
        return [ResumeResponse.model_validate(r) for r in resumes]

    async def create_resume(self, user_id: UUID, data: ResumeCreate) -> ResumeResponse:
        resume = await self.resume_repo.create(user_id, data.title, data.target_role, data.raw_text)
        return ResumeResponse.model_validate(resume)

    async def get_resume(self, user_id: UUID, resume_id: UUID) -> ResumeResponse:
        resume = await self.resume_repo.get_by_id(resume_id, user_id)
        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")
        return ResumeResponse.model_validate(resume)

    async def apply_suggestion(self, user_id: UUID, resume_id: UUID, suggestion_id: UUID) -> ResumeResponse:
        resume = await self.resume_repo.apply_suggestion(resume_id, suggestion_id, user_id)
        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Suggestion or resume not found.")
        return ResumeResponse.model_validate(resume)
