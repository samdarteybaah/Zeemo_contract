from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class ContractAnalysis(BaseModel):
    id : str | None = None 
    user_id : str 
    contract_text: str = Field(min_length=1)
    summary: Optional[str] = None
    risk_score : float = None
    created_at : datetime = Field(default_factory=datetime.now)

    def set_summary(self, summary: str):
        if not summary.strip():
            raise ValueError("Summary cannot be empty")
        self.summary = summary

    def set_risk_score(self, score: float):
        if not 0 <= score <= 1:
            raise ValueError("Risk score must be between 0 and 1")
        self.risk_score = score