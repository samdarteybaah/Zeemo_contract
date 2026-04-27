import re
from pydantic import  BaseModel, EmailStr, Field, field_validator
from datetime import datetime

class User(BaseModel):
    id : str | None = None 
    email : EmailStr
    name : str = Field(min_length=2, max_length=100)
    password_hash : str
    created_at : datetime = Field(default_factory=datetime.now)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value:str) -> str:
        pattern = r"^[A-Za-z\s\-']+$"
        if not re.match(pattern,value):
            raise ValueError("Name must contain only alphabetic characters")
        return value
    
    def verify_password(self, plain_password: str, hasher):
        # look to see if passwords match when logging in 
        return hasher.verify(plain_password, self.password_hash)


