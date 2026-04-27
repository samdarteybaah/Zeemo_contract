from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings
from app.infrastructure.logging.logger import logger


settings = get_settings()
client:  AsyncIOMotorClient | None = None
db = None 

async def connect_to_mongo():
    # call this connecting function whenever app is running 
    global client,db
    try:
        client = AsyncIOMotorClient(settings.DATABASE_URL)
        db = client.get_default_database()
        await db.command("ping")
        logger.info("MongoDB connection established")
    except Exception as e:
        logger.error("MongoDB connection failed", exc_info=True)
        raise e


async def close_mongo_connection():
    # call this connecting function whenever app is shutting down
    global client 
    if client:
        client.close()

