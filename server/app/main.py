from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.exception_handlers import http_exception_handler

# error and exception handling imports
from fastapi.exceptions import RequestValidationError
from pymongo.errors import PyMongoError
import asyncio
from contextlib import asynccontextmanager

from app.core.exception_handlers import (
    validation_exception_handler,
    database_exception_handler,
    ai_timeout_exception_handler,
    generic_exception_handler
)

from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.routes import health
from app.api.routes import analysis_routes, auth_routes, chat_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    print("MongoDB connected")

    yield

    await close_mongo_connection()
    print("MongoDB connection closed")


app = FastAPI(title="Zeemo API", version="1.0", lifespan=lifespan)

# middle ware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# call for exceptions
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(PyMongoError, database_exception_handler)
app.add_exception_handler(asyncio.TimeoutError, ai_timeout_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(health.router)
app.include_router(auth_routes.router)
app.include_router(analysis_routes.router)
app.include_router(chat_routes.router)