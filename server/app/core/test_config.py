from app.core.config import get_settings

settings = get_settings()
print(settings.DATABASE_URL)