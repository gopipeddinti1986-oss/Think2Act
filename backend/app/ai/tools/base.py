from abc import ABC, abstractmethod
from typing import Any, Dict
from uuid import UUID
from pydantic import BaseModel

class ToolResult(BaseModel):
    success: bool
    requires_confirmation: bool = False
    action_type: str
    target_type: str = "TASK"
    target_id: Any = None
    payload: Dict[str, Any]
    message: str

class BaseTool(ABC):
    name: str
    description: str
    parameters: Dict[str, Any]

    @abstractmethod
    async def execute(self, user_id: UUID, params: Dict[str, Any], confirmed: bool = False) -> ToolResult:
        pass