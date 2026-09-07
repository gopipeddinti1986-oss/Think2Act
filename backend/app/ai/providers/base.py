from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AIToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)

class AIProviderResponse(BaseModel):
    content: str
    tool_calls: List[AIToolCall] = Field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None

class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_response(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> AIProviderResponse:
        """Generate response from AI provider with optional tool calling."""
        pass
