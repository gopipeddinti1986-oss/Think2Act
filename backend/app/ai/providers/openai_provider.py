import json
import logging
from typing import List, Dict, Any, Optional
import httpx
from app.ai.providers.base import BaseAIProvider, AIProviderResponse, AIToolCall
from app.ai.providers.mock_provider import MockAIProvider

logger = logging.getLogger(__name__)

class OpenAICompatibleProvider(BaseAIProvider):
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1", model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model or "gpt-4o-mini"
        self.fallback = MockAIProvider()

    async def generate_response(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> AIProviderResponse:
        if not self.api_key:
            return await self.fallback.generate_response(system_prompt, messages, tools, context)

        chat_messages = [{"role": "system", "content": system_prompt}]
        for m in messages:
            chat_messages.append({"role": m.get("role", "user"), "content": m.get("content", "")})

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": chat_messages,
            "temperature": 0.3
        }

        if tools:
            formatted_tools = []
            for t in tools:
                formatted_tools.append({
                    "type": "function",
                    "function": {
                        "name": t.get("name"),
                        "description": t.get("description", ""),
                        "parameters": t.get("parameters", {"type": "object", "properties": {}})
                    }
                })
            payload["tools"] = formatted_tools

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
                if resp.status_code != 200:
                    logger.warning(f"OpenAI compatible API returned {resp.status_code}: {resp.text}, falling back.")
                    return await self.fallback.generate_response(system_prompt, messages, tools, context)

                data = resp.json()
                choice = data.get("choices", [{}])[0]
                message_obj = choice.get("message", {})
                content = message_obj.get("content") or ""

                tool_calls: List[AIToolCall] = []
                raw_tool_calls = message_obj.get("tool_calls", [])
                for tc in raw_tool_calls:
                    fn = tc.get("function", {})
                    fn_name = fn.get("name", "")
                    try:
                        args = json.loads(fn.get("arguments", "{}"))
                    except Exception:
                        args = {}
                    tool_calls.append(AIToolCall(name=fn_name, arguments=args))

                return AIProviderResponse(
                    content=content or "Action proposed based on execution state.",
                    tool_calls=tool_calls,
                    raw_response=data
                )
        except Exception as exc:
            logger.warning(f"Error calling OpenAI compatible endpoint ({exc}), falling back to mock provider.")
            return await self.fallback.generate_response(system_prompt, messages, tools, context)
