from typing import Dict, Any, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.tools.base import BaseTool, ToolResult
from app.ai.tools.task_tools import CreateTaskTool
from app.ai.tools.planner_tools import ScheduleTaskTool

class ToolManager:
    def __init__(self, db: AsyncSession):
        self.db = db
        self._tools: Dict[str, BaseTool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        create_task_tool = CreateTaskTool(self.db)
        schedule_task_tool = ScheduleTaskTool(self.db)

        self._tools[create_task_tool.name] = create_task_tool
        self._tools[schedule_task_tool.name] = schedule_task_tool

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            for tool in self._tools.values()
        ]

    async def execute_tool(
        self,
        tool_name: str,
        user_id: UUID,
        params: Dict[str, Any],
        confirmed: bool = False
    ) -> ToolResult:
        tool = self._tools.get(tool_name)
        if not tool:
            return ToolResult(
                success=False,
                action_type="UNKNOWN",
                payload={},
                message=f"Tool '{tool_name}' is not registered."
            )
        return await tool.execute(user_id=user_id, params=params, confirmed=confirmed)