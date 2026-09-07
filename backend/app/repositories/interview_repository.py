import re
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.interview import InterviewSession, InterviewQuestion

def evaluate_interview_answer(question_text: str, ideal_answer: str, user_answer: str) -> dict:
    if not user_answer or len(user_answer.strip()) < 5:
        return {
            "score": 20.0,
            "rubric_scores": {"correctness": 15, "clarity": 25, "completeness": 20},
            "ai_feedback": "Answer was too brief or incomplete. Please elaborate on core architectural mechanics and trade-offs."
        }

    stopwords = {"that", "with", "from", "this", "which", "will", "have", "more", "uses", "than", "rather", "other", "into", "their", "cost", "using", "does"}
    ideal_tokens = set(re.findall(r'[a-zA-Z0-9_\-\+]+', ideal_answer.lower())) - stopwords
    user_tokens = set(re.findall(r'[a-zA-Z0-9_\-\+]+', user_answer.lower()))

    # Correctness: token overlap with ideal answer
    matched = ideal_tokens.intersection(user_tokens)
    token_coverage = len(matched) / max(1, len(ideal_tokens))
    correctness = min(98.0, max(30.0, round(token_coverage * 120.0, 1)))

    # Completeness: answer length / conceptual detail
    len_ratio = min(1.0, len(user_answer.split()) / max(1, len(ideal_answer.split()) * 0.7))
    completeness = min(95.0, max(30.0, round(len_ratio * 100.0, 1)))

    # Clarity: structure and technical vocabulary
    has_technical_terms = len(matched) >= 2
    has_connectors = any(c in user_answer.lower() for c in ["because", "whereas", "while", "rather", "which", "however", "therefore", "delegat", ";"])
    clarity = 88.0 if (has_technical_terms and has_connectors) else 75.0 if has_technical_terms else 55.0

    overall_score = round(0.5 * correctness + 0.3 * completeness + 0.2 * clarity, 1)

    if overall_score >= 80.0:
        feedback = f"Strong architectural understanding demonstrated. Accurate identification of core principles ({', '.join(list(matched)[:3])})."
    elif overall_score >= 60.0:
        missing_concepts = list(ideal_tokens - user_tokens)[:3]
        feedback = f"Solid foundation demonstrated. To strengthen answer, also address: {', '.join(missing_concepts)}."
    else:
        feedback = "Answer covers basic intuition but misses key architectural mechanics. Review the topic's core failure modes and trade-offs."

    return {
        "score": overall_score,
        "rubric_scores": {
            "correctness": int(correctness),
            "clarity": int(clarity),
            "completeness": int(completeness)
        },
        "ai_feedback": feedback
    }

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
        
        evaluation = evaluate_interview_answer(q.question_text, q.ideal_answer or "", answer)
        q.user_answer = answer
        q.rubric_scores = evaluation["rubric_scores"]
        q.score = evaluation["score"]
        q.ai_feedback = evaluation["ai_feedback"]
        
        await self.db.commit()
        await self.db.refresh(q)
        return q
