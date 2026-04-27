from typing import Any, Dict, List, Optional
from bson import ObjectId

class BaseRepository:
    def __init__(self, db, collection_name: str):
        self.collection = db[collection_name]

    def serialise(self, doc_id):
        doc_id["_id"] = str(doc_id["_id"])
        return doc_id

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data.pop("id",None)
        result = await self.collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data

    async def get_by_id(self, document_id: str) -> Optional [Dict[str, Any]]:
        return await self.collection.find_one({"_id":ObjectId(document_id)})
    
    async def update(self, document_id: str, update_data: Dict[str, Any]) -> bool :
        result = await  self.collection.update_one(
            {"_id" : ObjectId(document_id)},
            {"$set" : update_data}
        ) 
        return result.modified_count > 0
    
    async def delete(self, document_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count > 0
    
    async def delete_all(self, document_id: str) -> bool:
        result = await self.collection.delete_many({"_id": ObjectId(document_id)})
        return result.deleted > 0
    
    async def find_many(self, filter_query: Dict[str, Any], sort=None) -> List[Dict[str, Any]]:
        cursor = self.collection.find(filter_query)
        if sort:
            cursor = cursor.sort(sort)
        docs = await cursor.to_list(length=None)
        for doc in docs:
            doc["_id"] = str(doc["_id"])
        return docs

