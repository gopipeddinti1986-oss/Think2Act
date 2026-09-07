from app.core.config import settings
from app.ai.providers.base import BaseAIProvider
from app.ai.providers.mock_provider import MockAIProvider
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.providers.openai_provider import OpenAICompatibleProvider

def get_ai_provider() -> BaseAIProvider:
    provider = (settings.AI_PROVIDER or "mock").lower()
    api_key = settings.AI_API_KEY or ""
    model = settings.AI_MODEL or ""

    if provider == "gemini" and api_key:
        return GeminiProvider(api_key=api_key, model=model or "gemini-1.5-flash")
    elif provider == "groq" and api_key:
        return OpenAICompatibleProvider(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            model=model or "llama-3.3-70b-versatile"
        )
    elif provider == "openai" and api_key:
        return OpenAICompatibleProvider(
            api_key=api_key,
            base_url="https://api.openai.com/v1",
            model=model or "gpt-4o-mini"
        )
    else:
        return MockAIProvider()
