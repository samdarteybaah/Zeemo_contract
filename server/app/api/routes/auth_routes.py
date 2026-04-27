from fastapi import APIRouter, Depends
from app.application.dtos.auth_dto import AuthResponseDTO, RegisterDTO, LoginDTO
from app.core.dependencies import get_register_use_case, get_login_use_case
from app.application.use_case.login_user_use_case import LoginUserUseCase
from app.application.use_case.register_user_use_case import RegisterUserUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
async def signup(
    user_data: RegisterDTO,
    register_use_case: RegisterUserUseCase = Depends(get_register_use_case)
):
    return await register_use_case.execute(user_data.email, user_data.name, user_data.password)

@router.post("/login")
async def login(
    credentials: LoginDTO,
    login_use_case: LoginUserUseCase = Depends(get_login_use_case)
):
    return await login_use_case.execute(credentials.email, credentials.password)