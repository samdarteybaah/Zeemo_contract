# server/app/infrastructure/ai/openai_provider.py
import json
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from app.infrastructure.ai.gpt_provider import GPTProvider


class OpenAIProvider(GPTProvider):
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            api_key=api_key,
            model="gpt-4",
        )
        self.parser = JsonOutputParser()

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