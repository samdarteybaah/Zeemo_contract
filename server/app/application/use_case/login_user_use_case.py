from fastapi import HTTPException, status

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.core.security import verify_password, create_access_token, hash_password 
from app.infrastructure.repository.user_repository import UserRepository
from app.application.dtos.auth_dto import AuthResponseDTO

class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    # fetch email
    async def execute(self, email:str, password:str)->AuthResponseDTO:
        user = await self.user_repository.find_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found")
        
        # verify password                          
        if not verify_password(password, user["password_hash"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
        
        # generate jwt token
        token = create_access_token({"sub": str(user["_id"])})

        # return dto
        return AuthResponseDTO(
            user_id = str(user["_id"]),
            name = user["name"],
            email = user["email"],
            access_token = token

        )