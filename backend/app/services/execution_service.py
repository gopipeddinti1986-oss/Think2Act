from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.models.entities import Task, TaskStatus, Goal, UserSkill, Evidence
from app.repositories.task_repository import TaskRepository
from app.repositories.goal_repository import GoalRepository

class ExecutionService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repo = TaskRepository(db)
        self.goal_repo = GoalRepository(db)

    def complete_task(self, task_id: int, user_id: int, actual_minutes: int) -> Task:
        task = self.task_repo.get_by_user_and_id(user_id=user_id, task_id=task_id)
        if not task:
            raise ValueError("Task not found")

        # 1. Update Task Execution Metadata
        task.status = TaskStatus.COMPLETED
        task.actual_duration_minutes = actual_minutes
        task.completed_at = datetime.utcnow()

        # 2. Re-evaluate Associated Goal Progress
        if task.goal_id:
            self._update_goal_progress(task.goal_id)

        # 3. Propagate Skill Improvement & Evidence Generation
        if task.skills:
            for skill in task.skills:
                self._generate_skill_evidence(user_id=user_id, task=task, skill_id=skill.id)

        self.db.commit()
        self.db.refresh(task)
        return task

    def _update_goal_progress(self, goal_id: int):
        goal = self.db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal or not goal.tasks:
            return

        total_tasks = len(goal.tasks)
        completed_tasks = sum(1 for t in goal.tasks if t.status == TaskStatus.COMPLETED)
        
        goal.calculated_progress = (completed_tasks / total_tasks) * 100.0

    def _generate_skill_evidence(self, user_id: int, task: Task, skill_id: int):
        user_skill = self.db.query(UserSkill).filter(
            UserSkill.user_id == user_id,
            UserSkill.skill_id == skill_id
        ).first()

        if not user_skill:
            user_skill = UserSkill(user_id=user_id, skill_id=skill_id, proficiency_score=10.0, confidence_score=10.0)
            self.db.add(user_skill)
            self.db.flush()

        # Create verifiable evidence unit
        evidence = Evidence(
            user_id=user_id,
            user_skill_id=user_skill.id,
            task_id=task.id,
            title=f"Completed: {task.title}",
            summary=f"Task completed in {task.actual_duration_minutes} minutes.",
            impact_weight=1.5 if task.actual_duration_minutes >= 60 else 1.0
        )
        self.db.add(evidence)

        # Increment proficiency and confidence deterministically
        user_skill.proficiency_score = min(100.0, user_skill.proficiency_score + (2.0 * evidence.impact_weight))
        user_skill.confidence_score = min(100.0, user_skill.confidence_score + (1.5 * evidence.impact_weight))