from pydantic import BaseModel, Field
from typing import Dict, Optional, List

class ContractRisk(BaseModel):
    summary: str
    risks: List[str]
    obligations: List[str]
    negotiation_suggestions: List[str]
    ambiguity_flags: List[str]

    # Optional scoring layer
    scores: Optional[Dict[str, int]] = Field(default=None)
    overall_score: Optional[float] = Field(default=None)