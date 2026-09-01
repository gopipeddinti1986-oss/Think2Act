from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repository import TaskRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.focus_repository import FocusRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.learning_repository import LearningRepository

class AIOrchestrator:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_repo = TaskRepository(db)
        self.goal_repo = GoalRepository(db)
        self.focus_repo = FocusRepository(db)
        self.skill_repo = SkillRepository(db)
        self.learning_repo = LearningRepository(db)

    async def gather_user_context(self, user_id: UUID) -> Dict[str, Any]:
        tasks = await self.task_repo.list_by_user(user_id, limit=10)
        total, completed, pending, rate = await self.task_repo.get_summary_counts(user_id)
        goals = await self.goal_repo.list_by_user(user_id)
        user_skills = await self.skill_repo.list_user_skills(user_id)
        _, focus_s, _, _ = await self.focus_repo.get_today_totals(user_id)

        return {
            "tasks_summary": {"total": total, "completed": completed, "pending": pending, "rate": rate},
            "recent_tasks": [{"id": str(t.id), "title": t.title, "priority": t.priority, "status": t.status} for t in tasks[:5]],
            "active_goals": [{"id": str(g.id), "title": g.title, "priority": g.priority} for g in goals[:3]],
            "skills": [{"id": str(s.skill_id), "name": s.skill.name if s.skill else "Skill", "level": float(s.level)} for s in user_skills[:5]],
            "today_focus_mins": int(focus_s / 60)
        }

    async def process_user_message(
        self,
        user_id: UUID,
        message: str
    ) -> Dict[str, Any]:
        ctx = await self.gather_user_context(user_id)
        msg_lower = message.lower()

        proposed_actions: List[Dict[str, Any]] = []
        response_text = ""

        # Intent 1: Asking what to do / plan today
        if any(w in msg_lower for w in ["what should i do", "what to do", "plan today", "prioritize", "schedule"]):
            pending_count = ctx["tasks_summary"]["pending"]
            skills_list = ctx["skills"]
            lowest_skill = sorted(skills_list, key=lambda s: s["level"])[0] if skills_list else None

            if pending_count > 0:
                top_task = ctx["recent_tasks"][0]
                response_text = (
                    f"Based on your current execution workload, you have **{pending_count} pending tasks**. "
                    f"I recommend tackling **'{top_task['title']}'** ({top_task['priority']} Priority) during your peak focus window. "
                )
                if lowest_skill:
                    response_text += f"Also, your **{lowest_skill['name']}** skill is currently at {lowest_skill['level']}/100, which has high leverage for your career roadmap."
                
                # Propose schedule action
                now = datetime.now(timezone.utc)
                start_slot = now + timedelta(hours=1)
                end_slot = start_slot + timedelta(minutes=45)
                proposed_actions.append({
                    "action_type": "SCHEDULE_TASK",
                    "target_type": "PLANNER",
                    "target_id": UUID(top_task["id"]),
                    "payload": {
                        "task_id": top_task["id"],
                        "task_title": top_task["title"],
                        "start_at": start_slot.isoformat(),
                        "end_at": end_slot.isoformat(),
                        "reason": f"Priority execution block ({top_task['priority']})"
                    },
                    "requires_confirmation": True
                })
            else:
                response_text = (
                    "All your scheduled tasks are currently clear! To maintain momentum, "
                    "I suggest creating a focused practice task targeting your core skill roadmap."
                )
                proposed_actions.append({
                    "action_type": "CREATE_TASK",
                    "target_type": "TASK",
                    "payload": {
                        "title": "Solve 3 Graph & Tree Algorithmic Problems",
                        "description": "Strengthen DSA evidence for technical interview preparation",
                        "priority": "HIGH",
                        "estimated_minutes": 60,
                        "category": "DSA"
                    },
                    "requires_confirmation": True
                })

        # Intent 2: User asking to create or learn something
        elif any(w in msg_lower for w in ["learn", "create task", "add task", "study"]):
            # Extract topic
            topic = "SQL Optimization" if "sql" in msg_lower else "Docker Deployment" if "docker" in msg_lower else "System Architecture"
            response_text = (
                f"I've structured a high-impact learning challenge for **{topic}**. "
                f"Completing this will add verified project evidence to your Skill Graph."
            )
            proposed_actions.append({
                "action_type": "CREATE_TASK",
                "target_type": "TASK",
                "payload": {
                    "title": f"Complete hands-on {topic} workshop & implementation",
                    "description": f"Practical exercise to close verified skill gap in {topic}",
                    "priority": "HIGH",
                    "estimated_minutes": 60,
                    "category": "Learning"
                },
                "requires_confirmation": True
            })

        # Intent 3: Productivity or progress review
        elif any(w in msg_lower for w in ["productivity", "progress", "performance", "how am i doing", "focus"]):
            total = ctx["tasks_summary"]["total"]
            rate = ctx["tasks_summary"]["rate"]
            focus_m = ctx["today_focus_mins"]
            response_text = (
                f"📊 **Performance Snapshot:**\n\n"
                f"- **Task Completion Rate:** {rate}% ({ctx['tasks_summary']['completed']}/{total} tasks)\n"
                f"- **Today's Focus Time:** {focus_m} minutes logged\n\n"
                f"Your execution is steady. To boost your productivity score, try pairing high-priority tasks with uninterrupted 45-minute focus intervals."
            )

        # General Coaching & Advice
        else:
            skills_summary = ", ".join([f"{s['name']} ({s['level']}/100)" for s in ctx["skills"][:3]])
            response_text = (
                f"I'm observing your system state: your tracked skills include **{skills_summary}**, "
                f"with **{ctx['tasks_summary']['pending']} pending tasks** today.\n\n"
                f"How would you like to direct your energy today? I can help you plan time blocks, close specific skill gaps, or schedule focused execution sprints."
            )

        return {
            "response_text": response_text,
            "proposed_actions": proposed_actions
        }
