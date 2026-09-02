from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.interview_repository import InterviewRepository
from app.repositories.evidence_repository import EvidenceRepository
from app.repositories.skill_repository import SkillRepository
from app.schemas.interview import InterviewSessionResponse, InterviewSessionCreate, SubmitAnswerRequest, InterviewQuestionResponse

class InterviewService:
    def __init__(self, db: AsyncSession):
        self.interview_repo = InterviewRepository(db)
        self.evidence_repo = EvidenceRepository(db)
        self.skill_repo = SkillRepository(db)

    async def list_sessions(self, user_id: UUID) -> List[InterviewSessionResponse]:
        sessions = await self.interview_repo.list_by_user(user_id)
        if not sessions:
            init_s = await self.interview_repo.create_session(user_id, "Backend Software Engineer", "TECHNICAL")
            return [InterviewSessionResponse.model_validate(init_s)]
        return [InterviewSessionResponse.model_validate(s) for s in sessions]

    async def start_session(self, user_id: UUID, data: InterviewSessionCreate) -> InterviewSessionResponse:
        session = await self.interview_repo.create_session(user_id, data.role_title, data.session_type)
        return InterviewSessionResponse.model_validate(session)

    async def get_session(self, user_id: UUID, session_id: UUID) -> InterviewSessionResponse:
        session = await self.interview_repo.get_by_id(session_id, user_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found.")
        return InterviewSessionResponse.model_validate(session)

    async def submit_answer(self, user_id: UUID, session_id: UUID, data: SubmitAnswerRequest) -> InterviewQuestionResponse:
        session = await self.interview_repo.get_by_id(session_id, user_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
        
        q = await self.interview_repo.submit_answer(session_id, data.question_id, data.answer)
        if not q:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")

        # Feed back into Evidence Graph if skill exists
        if q.target_skill:
            skill = await self.skill_repo.get_by_name(q.target_skill)
            if skill:
                await self.evidence_repo.create(
                    user_id=user_id,
                    skill_id=skill.id,
                    source_type="INTERVIEW",
                    strength=15.0,
                    description=f"Passed mock interview evaluation on '{q.target_skill}' with score {q.score}/100."
                )

        return InterviewQuestionResponse.model_validate(q)
