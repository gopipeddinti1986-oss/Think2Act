import json
import logging
from typing import List, Dict, Any, Optional
import httpx
from app.ai.providers.base import BaseAIProvider, AIProviderResponse, AIToolCall
from app.ai.providers.mock_provider import MockAIProvider

logger = logging.getLogger(__name__)

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model or "gemini-1.5-flash"
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

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        # Convert chat messages to Gemini contents format
        contents = []
        for m in messages:
            role = "user" if m.get("role") == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": m.get("content", "")}]
            })

        payload: Dict[str, Any] = {
            "contents": contents,
            "systemInstruction": {
                "parts": [{"text": system_prompt}]
            },
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 1000
            }
        }

        # If tools provided, format for Gemini functionDeclarations
        if tools:
            func_decls = []
            for t in tools:
                func_decls.append({
                    "name": t.get("name"),
                    "description": t.get("description", ""),
                    "parameters": t.get("parameters", {"type": "object", "properties": {}})
                })
            payload["tools"] = [{"functionDeclarations": func_decls}]

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code != 200:
                    logger.warning(f"Gemini API returned status {resp.status_code}: {resp.text}, falling back to mock.")
                    return await self.fallback.generate_response(system_prompt, messages, tools, context)

                data = resp.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    return await self.fallback.generate_response(system_prompt, messages, tools, context)

                parts = candidates[0].get("content", {}).get("parts", [])
                text_content = ""
                tool_calls: List[AIToolCall] = []

                for part in parts:
                    if "text" in part:
                        text_content += part["text"]
                    if "functionCall" in part:
                        fn = part["functionCall"]
                        tool_calls.append(AIToolCall(
                            name=fn.get("name", ""),
                            arguments=fn.get("args", {})
                        ))

                return AIProviderResponse(
                    content=text_content or "Action proposed based on execution state.",
                    tool_calls=tool_calls,
                    raw_response=data
                )
        except Exception as exc:
            logger.warning(f"Failed to communicate with Gemini API ({exc}), falling back to mock provider.")
            return await self.fallback.generate_response(system_prompt, messages, tools, context)
