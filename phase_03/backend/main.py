"""Main application entry point for the AI Chatbot with MCP application."""

import sys
import os
# Add the src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from src.models.base_models import User
from src.db import get_db
from src.agents.chat_agent import ChatAgent
from src.services.message_service import get_or_create_conversation, store_user_message, store_assistant_message
from src.services.conversation_service import ConversationService
from src.utils.error_handlers import (
    log_request_middleware,
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from routes.tasks import router as tasks_router
from src.api.routes.chat import router as chat_router
from src.api.middleware.auth_middleware import auth_middleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Starting up the AI Chatbot with MCP application...")

    # Initialize database tables
    # Use the database URL from settings which handles environment-specific configurations
    from src.db import init_db
    init_db()

    yield

    # Shutdown
    print("Shutting down the AI Chatbot with MCP application...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.middleware("http")(log_request_middleware)
app.middleware("http")(auth_middleware)

# Add exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
from routes.auth import router as auth_router
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(chat_router)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AI Chatbot with MCP"}

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the AI Chatbot with MCP API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True if settings.environment == "development" else False
    )