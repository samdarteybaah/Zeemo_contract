from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.infrastructure.repository.user_repository import UserRepository
from app.domain.entities.user import User
from app.core.security import hash_password
from app.application.dtos.auth_dto import AuthResponseDTO


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, email: str, name: str, password: str) -> AuthResponseDTO:
       
        # ensure user does not already exist
        existing_user = await self.user_repository.find_by_email(email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User with this email already exists.")

        # hash passwords                           
        hashed_password = hash_password(password)

        # create the entity/instance of a user class
        user = User(
            email=email,
            name = name,
            password_hash=hashed_password,
        )

        # add user to db
        created_user = await self.user_repository.create_user(user.model_dump())

        # return dto
        return AuthResponseDTO(
            user_id = str(created_user["_id"]),
            name = created_user["name"],
            email = created_user["email"]
        )

    

