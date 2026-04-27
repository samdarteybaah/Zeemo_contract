from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal,List
import uuid

class ChatMessage(BaseModel):
    user_id : str
    role : Literal["user", "assistant"]
    content:str = Field(min_length=1)
    timestamp : datetime = Field(default_factory=datetime.now)

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        if not value.strip():
            ValueError ("Message cannot be empty")
        return value

class ChatHistory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), exclude=True) 
    user_id : str
    title : str = Field(min_length=1, max_length=100)
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at : datetime = Field(default_factory=datetime.now)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value : str) -> str:
        if not value.strip():
            ValueError ("Title cannot be empty")
        return value
    
    def add_message(self, message: ChatMessage):
        if message.user_id != self.user_id:
            raise ValueError("Message user_id does not match chat history")
        self.messages.append(message)

    def total_messages(self) -> int:
        return len(self.messages)