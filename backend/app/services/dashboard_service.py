from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repository import TaskRepository
from app.repositories.goal_repository import GoalRepository
from app.models.user import User
from app.schemas.dashboard import DashboardResponse, TasksSummary, AISuggestion
from app.schemas.auth import AuthUserResponse
from app.schemas.goal import GoalResponse
from app.schemas.task import TaskResponse

class DashboardService:
    def __init__(self, db: AsyncSession):
        self.task_repo = TaskRepository(db)
        self.goal_repo = GoalRepository(db)

    async def get_dashboard_summary(self, user: User) -> DashboardResponse:
        total, completed, pending, rate = await self.task_repo.get_summary_counts(user.id)
        next_action_model = await self.task_repo.get_next_action(user.id)
        
        # Recent/Today's tasks (up to 5)
        recent_tasks = await self.task_repo.list_by_user(user.id, limit=5)
        goals = await self.goal_repo.list_by_user(user.id)

        # Dynamic AI suggestion rule based on current state
        if total == 0:
            ai_suggestion = AISuggestion(
                title="Welcome to Think2Act",
                message="Turn your first goal into actionable tasks to start building your execution momentum.",
                action_label="Create Goal",
                action_type="CREATE_GOAL"
            )
        elif pending > 5:
            ai_suggestion = AISuggestion(
                title="Workload Focus",
                message=f"You have {pending} pending tasks. Focus on high priority items to prevent task overload.",
                action_label="Focus Mode",
                action_type="START_FOCUS"
            )
        elif completed > 0 and pending == 0:
            ai_suggestion = AISuggestion(
                title="All Caught Up",
                message="Great execution! All scheduled tasks are complete. Consider planning next milestones.",
                action_label="Add Task",
                action_type="CREATE_TASK"
            )
        else:
            ai_suggestion = AISuggestion(
                title="Execution Flow",
                message="Execute your current high-priority task with a dedicated focus block.",
                action_label="Start Focus",
                action_type="START_FOCUS"
            )

        # Productivity score placeholder rule for Milestone 1 (deterministic)
        productivity_score = rate if total > 0 else 0

        return DashboardResponse(
            user=AuthUserResponse.model_validate(user),
            tasks_summary=TasksSummary(
                total=total,
                completed=completed,
                pending=pending,
                completion_rate=rate
            ),
            productivity_score=productivity_score,
            focus_minutes_today=0,
            readiness_score=75,
            next_action=TaskResponse.model_validate(next_action_model) if next_action_model else None,
            today_tasks=[TaskResponse.model_validate(t) for t in recent_tasks],
            goals=[GoalResponse.model_validate(g) for g in goals[:4]],
            ai_suggestion=ai_suggestion
        )
