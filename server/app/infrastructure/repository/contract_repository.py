from typing import List, Dict, Any, Optional
from app.infrastructure.repository.base_repository import BaseRepository


class ContractRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "contract_analyses")

    async def save_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.create(analysis_data.model_dump())
    
    async def get_analysis_by_id(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        return await self.get_by_id(analysis_id)
    
    async def get_user_analyses(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.find_many({"user_id": user_id})
    
    async def update_analysis(self, analysis_id: str, update_data: Dict[str, Any]) -> bool:
        return await self.update(analysis_id, update_data)
