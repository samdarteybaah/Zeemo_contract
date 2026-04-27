from app.infrastructure.ai.openai_provider import OpenAIProvider
from app.infrastructure.ai.gpt_provider import GPTProvider
from app.core.config import get_settings

def get_gpt_provider() -> GPTProvider: 
    settings = get_settings()
    return OpenAIProvider(api_key=settings.OPENAI_API_KEY)