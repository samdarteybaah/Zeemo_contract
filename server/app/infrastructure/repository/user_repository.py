from typing import Any, Dict, List, Optional
from app.infrastructure.repository.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "users")

    async def find_by_email(self, email: str)-> Optional[Dict[str , Any]]:
        return await self.collection.find_one({"email" : email})
    
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.create(user_data)

    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return await super().get_by_id(user_id)