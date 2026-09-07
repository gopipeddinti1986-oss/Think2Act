# Re-export canonical entity models to eliminate duplicate declarative registrations
from app.models.goal import Goal, PriorityEnum
from app.models.task import Task, TaskStatus
from app.models.skill import Skill, UserSkill, Evidence, TaskSkill, task_skills, SkillHistory

__all__ = [
    "Goal",
    "PriorityEnum",
    "Task",
    "TaskStatus",
    "Skill",
    "UserSkill",
    "Evidence",
    "TaskSkill",
    "task_skills",
    "SkillHistory",
]