from typing import Any, Dict, List, Optional
from bson import ObjectId
from app.infrastructure.repository.base_repository import BaseRepository

class ChatRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "chat_history")

    async def create_conversation(self, conversation_data: Dict[str, Any]):
        return await self.create(conversation_data)
    
    async def get_conversation(self, conversation_id: str):
        return await self.get_by_id(conversation_id)
    
    async def add_message(self, conversation_id: str, message: Dict[str, Any]):

        result = await self.collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$push": {"messages": message}}
        )

        return result.modified_count > 0
    
    async def get_user_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.find_many({"user_id": user_id},sort=[("created_at", 1)])

    async def delete_conversation(self, conversation_id: str):
        return await self.delete({"id": conversation_id})
    
    async def get_messages(self, conversation_id: str) -> List[Dict[str, Any]]:
        conversation = await self.get_by_id(conversation_id)
        if not conversation:
            return []
        return conversation.get("messages", [])
    
    async def find_one(self, query: Dict[str, Any]):
        doc = await self.collection.find_one(query)
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc