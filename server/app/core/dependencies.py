from functools import lru_cache
from app.infrastructure.repository.chat_repository import ChatRepository
from app.infrastructure.repository.user_repository import UserRepository
from app.infrastructure.repository.contract_repository import ContractRepository

from app.domain.services.contract_analyser import ContractAnalyser
from app.infrastructure.ai.groq_provider import GroqProvider
from app.application.use_case.chat_use_case import ChatUseCase
from app.application.use_case.analyse_contract_use_case import AnalyseContractUseCase
from app.application.use_case.register_user_use_case import RegisterUserUseCase
from app.application.use_case.login_user_use_case import LoginUserUseCase
from app.core.config import get_settings
from app.core.database import db


def get_database():
    # Provides the MongoDB database instance.
    return db


def get_chat_use_case() -> ChatUseCase:
    from app.core.database import db
    gpt_provider  = GroqProvider()
    return ChatUseCase(chat_repo=ChatRepository(db), gpt_provider=gpt_provider)


def get_analyse_use_case() -> AnalyseContractUseCase:
    from app.core.database import db
    gpt_provider  = GroqProvider()

    return AnalyseContractUseCase(
        user_repo=UserRepository(db),
        contract_repo=ContractRepository(db),
        chat_repo=ChatRepository(db),
        analyser=ContractAnalyser(ai_provider=gpt_provider)
    )


def get_register_use_case() -> RegisterUserUseCase:
    from app.core.database import db
    return RegisterUserUseCase(user_repository=UserRepository(db))


def get_login_use_case() -> LoginUserUseCase:
    from app.core.database import db
    return LoginUserUseCase(user_repository=UserRepository(db))