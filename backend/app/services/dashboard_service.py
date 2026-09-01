from uuid import UUID
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repository import TaskRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.focus_repository import FocusRepository
from app.repositories.productivity_repository import ProductivityRepository
from app.models.user import User
from app.schemas.dashboard import DashboardResponse, TasksSummary, AISuggestion
from app.schemas.auth import AuthUserResponse
from app.schemas.goal import GoalResponse
from app.schemas.task import TaskResponse

class DashboardService:
    def __init__(self, db: AsyncSession):
        self.task_repo = TaskRepository(db)
        self.goal_repo = GoalRepository(db)
        self.focus_repo = FocusRepository(db)
        self.productivity_repo = ProductivityRepository(db)

    async def get_dashboard_summary(self, user: User) -> DashboardResponse:
        total, completed, pending, rate = await self.task_repo.get_summary_counts(user.id)
        next_action_model = await self.task_repo.get_next_action(user.id)
        
        # Recent/Today's tasks (up to 5)
        recent_tasks = await self.task_repo.list_by_user(user.id, limit=5)
        goals = await self.goal_repo.list_by_user(user.id)

        # Real today's focus totals
        _, focus_s, distract_s, focus_ratio = await self.focus_repo.get_today_totals(user.id)
        today_focus_mins = int(focus_s / 60)

        # Real today productivity score
        productivity_score = round(0.5 * rate + 0.5 * focus_ratio, 1) if (total > 0 or focus_s > 0) else 0

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
                message=f"You have {pending} pending tasks. Schedule a focus session for your highest priority task.",
                action_label="Focus Mode",
                action_type="START_FOCUS"
            )
        elif completed > 0 and pending == 0:
            ai_suggestion = AISuggestion(
                title="All Caught Up",
                message="Great execution! All scheduled tasks are complete. Review your progress in analytics.",
                action_label="View Progress",
                action_type="VIEW_PROGRESS"
            )
        else:
            ai_suggestion = AISuggestion(
                title="Execution Momentum",
                message="Your focus is strongest when doing dedicated 45-minute sprint blocks.",
                action_label="Start Focus",
                action_type="START_FOCUS"
            )

        return DashboardResponse(
            user=AuthUserResponse.model_validate(user),
            tasks_summary=TasksSummary(
                total=total,
                completed=completed,
                pending=pending,
                completion_rate=rate
            ),
            productivity_score=int(productivity_score),
            focus_minutes_today=today_focus_mins,
            readiness_score=75,
            next_action=TaskResponse.model_validate(next_action_model) if next_action_model else None,
            today_tasks=[TaskResponse.model_validate(t) for t in recent_tasks],
            goals=[GoalResponse.model_validate(g) for g in goals[:4]],
            ai_suggestion=ai_suggestion
        )
