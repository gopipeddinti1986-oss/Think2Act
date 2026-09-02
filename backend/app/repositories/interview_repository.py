from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.interview import InterviewSession, InterviewQuestion

class InterviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user(self, user_id: UUID) -> List[InterviewSession]:
        result = await self.db.execute(
            select(InterviewSession).where(InterviewSession.user_id == user_id).order_by(desc(InterviewSession.created_at))
        )
        return list(result.scalars().all())

    async def get_by_id(self, session_id: UUID, user_id: UUID) -> Optional[InterviewSession]:
        result = await self.db.execute(
            select(InterviewSession).where(InterviewSession.id == session_id, InterviewSession.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_session(self, user_id: UUID, role_title: str, session_type: str = "TECHNICAL") -> InterviewSession:
        session = InterviewSession(
            user_id=user_id,
            role_title=role_title,
            session_type=session_type,
            status="IN_PROGRESS"
        )
        self.db.add(session)
        await self.db.flush()

        # Seed technical interview questions
        questions = [
            InterviewQuestion(
                session_id=session.id,
                question_text="How does Python's GIL impact asynchronous I/O compared to CPU-bound multiprocessing, and how would you design a scalable FastAPI architecture?",
                target_skill="Python",
                difficulty="HARD",
                ideal_answer="Asyncio uses single-threaded non-blocking event loop which yields control during network/DB I/O, bypassing GIL bottlenecks. For CPU-bound tasks, delegate to ProcessPoolExecutor or background worker queues like Celery/Redis."
            ),
            InterviewQuestion(
                session_id=session.id,
                question_text="Explain PostgreSQL MVCC and the operational trade-offs between Read Committed and Serializable isolation levels in a distributed ledger.",
                target_skill="SQL & PostgreSQL",
                difficulty="HARD",
                ideal_answer="MVCC creates new tuple versions rather than locking read rows. Read Committed allows non-repeatable reads; Serializable prevents anomalies via serialization graph checking at the cost of potential transaction retry aborts."
            ),
            InterviewQuestion(
                session_id=session.id,
                question_text="Design a resilient rate-limiting middleware using Redis sliding window log for high-traffic REST APIs.",
                target_skill="System Architecture",
                difficulty="MEDIUM",
                ideal_answer="Use Redis Sorted Sets (ZSET) with timestamps as scores. Remove elements older than (now - window), count remaining entries with ZCARD, and conditionally reject or ZADD current timestamp atomically with pipeline."
            )
        ]
        for q in questions:
            self.db.add(q)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def submit_answer(self, session_id: UUID, question_id: UUID, answer: str) -> Optional[InterviewQuestion]:
        result = await self.db.execute(
            select(InterviewQuestion).where(InterviewQuestion.id == question_id, InterviewQuestion.session_id == session_id)
        )
        q = result.scalar_one_or_none()
        if not q:
            return None
        
        q.user_answer = answer
        q.rubric_scores = {
            "correctness": 88,
            "clarity": 85,
            "completeness": 90
        }
        q.score = 87.5
        q.ai_feedback = "Strong architectural understanding demonstrated. Accurate distinction between event loop I/O multiplexing and multi-core CPU scheduling."
        await self.db.commit()
        await self.db.refresh(q)
        return q
