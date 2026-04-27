# server/app/infrastructure/ai/prompt_templates.py
from langchain_core.prompts import PromptTemplate


class ContractPromptTemplates:
    SYSTEM_ROLE: str = "Contract Risk Analyst"

    risk_analysis = PromptTemplate(
        input_variables=["user_contract_text", "system_role"],
        template="""
You are a {system_role}.

Analyze the following contract and return ONLY a valid JSON object with EXACTLY these 5 keys:
- "summary": a 2-3 sentence plain English overview
- "risks": a list of at least 3 strings, each describing a specific risk
- "obligations": a list of at least 3 strings, each describing a key obligation
- "negotiation_suggestions": a list of at least 2 strings, each suggesting a clause to renegotiate
- "ambiguity_flags": a list of at least 2 strings, each describing a vague clause

You MUST include all 5 keys. Do NOT return a partial response.
Do NOT include markdown, code blocks, or any text outside the JSON object.

Example format:
{{
  "summary": "...",
  "risks": ["...", "..."],
  "obligations": ["...", "..."],
  "negotiation_suggestions": ["...", "..."],
  "ambiguity_flags": ["...", "..."]
}}

Contract Text:
\"\"\"{user_contract_text}\"\"\"

Return ONLY the JSON object:
""".strip()
)

    short_summary = PromptTemplate(
        input_variables=["user_contract_text"],
        template="""
You are a {system_role}.
Summarize the key contract risks in the areas of:
- Liability
- Termination
- Payment terms
- Intellectual property
- Ambiguity

Return a short JSON object with keys:
"liability", "termination", "payment_terms", "intellectual_property", "ambiguity".

Contract Text:
\"\"\"{user_contract_text}\"\"\"

Important: Return ONLY JSON.
""".strip()
    )
