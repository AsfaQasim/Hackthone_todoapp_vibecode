"""Main application entry point for the AI Chatbot with MCP application."""

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
from .api.routes.chat import router as chat_router
from .api.middleware.auth_middleware import auth_middleware
from .utils.error_handlers import (
    log_request_middleware,
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .models.base_models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Starting up the AI Chatbot with MCP application...")
    
    # Initialize database tables
    engine = create_engine(settings.database_url.replace("+asyncpg", ""))
    Base.metadata.create_all(bind=engine)
    
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