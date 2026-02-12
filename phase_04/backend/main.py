"""Main application entry point for the AI Chatbot with MCP application."""

import sys
import os

# Add the src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings

from src.utils.error_handlers import (
    log_request_middleware,
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)

from routes.tasks import router as tasks_router
from src.api.routes.chat_simple import router as chat_router  # Using chat_simple with OpenAI
from src.api.routes.tasks_simple import router as tasks_simple_router  # Simplified tasks endpoint
from routes.auth import router as auth_router
from routes.tasks_by_email import router as tasks_by_email_router  # Simple tasks by email

from src.api.middleware.auth_middleware import auth_middleware
from src.middleware.json_response_middleware import JsonResponseMiddleware

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


# ==============================
# Lifespan
# ==============================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting AI Chatbot MCP...")

    from src.db import init_db
    init_db()

    yield

    print("Shutting down AI Chatbot MCP...")


# ==============================
# App
# ==============================

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan
)

# ==============================
# Middleware
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_request_middleware)
app.middleware("http")(auth_middleware)
app.add_middleware(JsonResponseMiddleware)

# ==============================
# Exception Handlers
# ==============================

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# ==============================
# Routers
# ==============================

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(tasks_simple_router)  # Simplified tasks endpoint (no user_id in path)
app.include_router(tasks_by_email_router)  # Simple tasks by email
app.include_router(chat_router)  # Chat router already has /api prefix

# ==============================
# Routes
# ==============================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Chatbot with MCP"}

@app.get("/")
async def root():
    return {"message": "Welcome to AI Chatbot MCP API"}


# ==============================
# Run
# ==============================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True if settings.environment == "development" else False
    )
