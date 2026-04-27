from typing import Any
from app.infrastructure.ai.gpt_provider import GPTProvider
from app.domain.entities.contract_risk import ContractRisk
from app.domain.schemas.contract_risk_schema import ContractRiskSchema
from app.infrastructure.ai.prompt_templates import ContractPromptTemplates
from app.domain.services.risk_scorer import RiskScorer
from pydantic import ValidationError


class ContractAnalyser:
    def __init__(self, ai_provider: GPTProvider):
        self.ai_provider = ai_provider

    async def analyze(self, contract_text: str) -> ContractRisk:

        # input validation
        if not contract_text or len(contract_text) < 20:
            raise ValueError("Contract text is too short to analyse.")

        if len(contract_text) > 10000:
            raise ValueError("Contract text exceeds maximum allowed length.")

        for attempt in range(2):
            # calling GPT via LangChain chain
            raw_response: Any = await self.ai_provider.generate(
                prompt_template=ContractPromptTemplates.risk_analysis,
                input_variables={"user_contract_text": contract_text}
            )

            # validating GPT output
            try:
                validated = ContractRiskSchema(**raw_response)
                break
            except ValidationError as e:
                if attempt == 1:
                    raise ValueError(f"Invalid GPT output: {e}") from e

        # converting validated schema to dictionary
        risk_dict = validated.model_dump()

        # calculating scores
        scores = RiskScorer.calculate_scores(risk_dict)
        overall = RiskScorer.calculate_overall(scores)

        return ContractRisk(
            **risk_dict,
            scores=scores,
            overall_score=overall
        )