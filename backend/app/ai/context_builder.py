from typing import Dict, Any, List
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.focus_repository import FocusRepository
from app.repositories.skill_repository import SkillRepository
from app.services.learning_service import LearningService

class ContextBuilder:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.task_repo = TaskRepository(db)
        self.goal_repo = GoalRepository(db)
        self.focus_repo = FocusRepository(db)
        self.skill_repo = SkillRepository(db)
        self.learning_svc = LearningService(db)

    async def build_user_context(self, user_id: UUID) -> Dict[str, Any]:
        user = await self.user_repo.get_by_id(user_id)
        profile = getattr(user, "profile", None)

        total, completed, pending, rate = await self.task_repo.get_summary_counts(user_id)
        tasks = await self.task_repo.list_by_user(user_id, limit=10)
        pending_tasks = [t for t in tasks if str(t.status) not in ("COMPLETED", "CANCELLED")]

        goals = await self.goal_repo.list_by_user(user_id)
        active_goals = [g for g in goals if getattr(g, "status", "ACTIVE") == "ACTIVE"]

        user_skills = await self.skill_repo.list_user_skills(user_id)
        _, focus_s, _, focus_ratio = await self.focus_repo.get_today_totals(user_id)
        today_focus_mins = int(focus_s / 60)

        # Retrieve real skill gaps if any
        skill_gaps_summary: List[Dict[str, Any]] = []
        try:
            gap_report = await self.learning_svc.compute_skill_gaps(user_id)
            for g in gap_report.gaps[:5]:
                skill_gaps_summary.append({
                    "skill_name": g.skill_name,
                    "gap": g.gap,
                    "severity": g.severity,
                    "current_level": g.current_level,
                    "required_level": g.required_level
                })
        except Exception:
            pass

        return {
            "user": {
                "name": getattr(user, "name", "User"),
                "target_role": getattr(profile, "target_role", "Software Engineer") or "Software Engineer",
                "preferred_sprint_minutes": getattr(profile, "preferred_sprint_minutes", 45) or 45,
                "work_start_time": getattr(profile, "work_start_time", "09:00") or "09:00",
                "work_end_time": getattr(profile, "work_end_time", "18:00") or "18:00"
            },
            "tasks_summary": {
                "total": total,
                "completed": completed,
                "pending": pending,
                "rate": rate
            },
            "recent_tasks": [
                {
                    "id": str(t.id),
                    "title": t.title,
                    "priority": getattr(t, "priority", "MEDIUM"),
                    "status": str(t.status),
                    "estimated_minutes": getattr(t, "estimated_minutes", 45) or 45
                }
                for t in pending_tasks[:5]
            ],
            "active_goals": [
                {
                    "id": str(g.id),
                    "title": g.title,
                    "priority": getattr(g, "priority", "HIGH"),
                    "progress": getattr(g, "calculated_progress", 0)
                }
                for g in active_goals[:3]
            ],
            "skills": [
                {
                    "id": str(s.skill_id),
                    "name": s.skill.name if s.skill else "Skill",
                    "level": float(s.level)
                }
                for s in user_skills[:6]
            ],
            "skill_gaps": skill_gaps_summary,
            "today_focus_mins": today_focus_mins,
            "focus_ratio": focus_ratio
        }