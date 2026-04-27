from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    """
    Central configuration class for Zeemo.

    Loads environment variables from .env
    Validates required fields
    Exposes typed settings globally
    """

    # Environment
    ENVIRONMENT: str = Field(default="development")

    # Database
    DATABASE_URL: str

    # JWT Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # AI Provider
    GROQ_API_KEY: str
    GROQ_MODEL: str
    
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_TEMPERATURE: float = 0.2
    OPENAI_MAX_TOKENS: int = 1500

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()