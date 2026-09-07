from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.entities import UserSkill, Skill, Task, TaskStatus, PriorityEnum, Evidence
from app.services.skill_service import SkillService

class InterviewFeedbackService:
    def __init__(self, db: Session):
        self.db = db
        self.skill_service = SkillService(db)

    def process_interview_results(
        self,
        user_id: int,
        session_title: str,
        evaluations: List[Dict[str, Any]] # e.g., [{"skill_name": "SQL", "score": 40.0, "notes": "Weak on JOIN optimizations"}]
    ) -> Dict[str, Any]:
        
        updated_skills = []
        created_tasks = []

        for eval_item in evaluations:
            skill_name = eval_item["skill_name"]
            score = eval_item["score"] # 0 to 100
            notes = eval_item.get("notes", "")

            skill_obj = self.db.query(Skill).filter(Skill.name.ilike(skill_name)).first()
            if not skill_obj:
                continue

            user_skill = (
                self.db.query(UserSkill)
                .filter(UserSkill.user_id == user_id, UserSkill.skill_id == skill_obj.id)
                .first()
            )

            if not user_skill:
                user_skill = UserSkill(user_id=user_id, skill_id=skill_obj.id, proficiency_score=score, confidence_score=20.0)
                self.db.add(user_skill)
                self.db.flush()

            # Record Interview Evidence
            evidence = Evidence(
                user_id=user_id,
                user_skill_id=user_skill.id,
                title=f"Mock Interview: {session_title}",
                summary=f"Score: {score}%. Feedback: {notes}",
                impact_weight=1.0 if score >= 70.0 else -0.5 # Penalty for poor interview performance
            )
            self.db.add(evidence)

            # Recalculate skill standing
            self.skill_service.recalculate_skill_from_evidence(user_id, skill_obj.id)
            updated_skills.append(skill_name)

            # If weakness detected (score < 60%), automatically spawn remediation task
            if score < 60.0:
                remediation_task = Task(
                    user_id=user_id,
                    title=f"Remediate {skill_name}: {session_title} Weakness",
                    description=f"Interview Feedback Note: {notes}",
                    priority=PriorityEnum.URGENT,
                    status=TaskStatus.PENDING,
                    estimated_duration_minutes=60
                )
                remediation_task.skills.append(skill_obj)
                self.db.add(remediation_task)
                self.db.flush()
                created_tasks.append(remediation_task.id)

        self.db.commit()

        return {
            "session_title": session_title,
            "skills_updated": updated_skills,
            "remediation_tasks_created": len(created_tasks),
            "task_ids": created_tasks
        }