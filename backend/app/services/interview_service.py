from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.interview_repository import InterviewRepository
from app.repositories.evidence_repository import EvidenceRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.activity_repository import ActivityRepository
from app.schemas.interview import InterviewSessionResponse, InterviewSessionCreate, SubmitAnswerRequest, InterviewQuestionResponse

class InterviewService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.interview_repo = InterviewRepository(db)
        self.evidence_repo = EvidenceRepository(db)
        self.skill_repo = SkillRepository(db)
        self.activity_repo = ActivityRepository(db)

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

        # Feed back into Evidence & Skill Graph if skill exists
        if q.target_skill and q.score >= 40.0:
            skill = await self.skill_repo.get_by_name(q.target_skill)
            if skill:
                evidence = await self.evidence_repo.create(
                    user_id=user_id,
                    skill_id=skill.id,
                    source_type="INTERVIEW",
                    strength=round(q.score / 5.0, 1),
                    description=f"Completed technical interview question on '{q.target_skill}' with score {q.score}/100."
                )
                from app.services.skill_service import SkillService
                await SkillService(self.db).record_evidence(
                    user_id=user_id,
                    skill_id=skill.id,
                    evidence_id=evidence.id,
                    evidence_type="INTERVIEW",
                    points=float(round(q.score / 5.0, 1))
                )

        # Emit activity event
        await self.activity_repo.create_event(
            user_id=user_id,
            event_type="INTERVIEW_QUESTION_ANSWERED",
            title=f"Interview question answered for {session.role_title}",
            description=f"Score: {q.score}/100",
            entity_type="INTERVIEW_QUESTION",
            entity_id=q.id,
            payload={"session_id": str(session_id), "score": q.score, "rubric": q.rubric_scores}
        )
        await self.db.commit()

        return InterviewQuestionResponse.model_validate(q)
