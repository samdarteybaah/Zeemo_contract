from fastapi import APIRouter
from app.core.database import db

router = APIRouter()

@router.get("/health", tags=['Health'])
async def health_check():
    try:
        await db.command("ping")
        return {"status":"healthy"}
    except Exception as e:
        return {"status": "unhealthy", "detail": str(e)}