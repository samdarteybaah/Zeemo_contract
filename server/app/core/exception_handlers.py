from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pymongo.errors import PyMongoError
import asyncio

from app.infrastructure.logging.logger import logger


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")

    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": "Invalid request data",
            "details": exc.errors()
        }
    )


async def database_exception_handler(request: Request, exc: PyMongoError):
    logger.error(f"Database error: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "DatabaseError",
            "message": "A database error occurred",
            "details": None
        }
    )

async def ai_timeout_exception_handler(request: Request, exc: asyncio.TimeoutError):
    
    logger.error("AI provider timeout")

    return JSONResponse(
        status_code=504,
        content={
            "error": "AITimeout",
            "message": "AI service took too long to respond",
            "details": None
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "details": str(exc)
        }
    )