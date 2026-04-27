from pydantic import BaseModel, ConfigDict, Field
from typing import List

class ContractRiskSchema(BaseModel):
    summary: str
    risks: List[str] = Field(default_factory=list)
    obligations: List[str] = Field(default_factory=list)
    negotiation_suggestions: List[str] = Field(default_factory=list)
    ambiguity_flags: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="ignore") 