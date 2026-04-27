# server/app/infrastructure/ai/groq_provider.py
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from app.infrastructure.ai.gpt_provider import GPTProvider
from app.core.config import get_settings

settings = get_settings()

class GroqProvider(GPTProvider):
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
            model=settings.GROQ_MODEL,
        )

    async def generate(
        self,
        prompt_template,
        input_variables: dict,
        temperature: float = 0.7,
        max_tokens: int = 512,
        parse_json: bool = True,
        retry: int = 2,
        **kwargs
    ) -> dict | str:

        self.llm.temperature = temperature
        self.llm.max_tokens = max_tokens

        parser = JsonOutputParser() if parse_json else StrOutputParser()
        chain = prompt_template | self.llm | parser

        for attempt in range(retry + 1):
            try:
                return await chain.ainvoke({
                    **input_variables,
                    "system_role": "Contract Risk Analyst"
                })
            except Exception as e:
                if attempt == retry:
                    raise e
                await asyncio.sleep(0.7)