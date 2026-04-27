from pydantic import BaseModel, EmailStr

class RegisterDTO(BaseModel):
    email: EmailStr
    name: str
    password: str

class LoginDTO(BaseModel):
    email: EmailStr
    password: str

class AuthResponseDTO(BaseModel):
    user_id: str
    name : str
    email: str
    access_token: str | None = None