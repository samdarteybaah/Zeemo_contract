from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.dependencies.auth import get_current_user
from app.application.use_case.analyse_contract_use_case import AnalyseContractUseCase
from app.core.dependencies import get_analyse_use_case

router = APIRouter(prefix="/analysis", tags=["analysis"])

class AnalysisRequest(BaseModel):
    contract_text: str

@router.post("/")
async def analyze_contract(
    body: AnalysisRequest,
    current_user=Depends(get_current_user),
    analyse_use_case: AnalyseContractUseCase = Depends(get_analyse_use_case)
):
    return await analyse_use_case.execute(str(current_user["_id"]), body.contract_text)