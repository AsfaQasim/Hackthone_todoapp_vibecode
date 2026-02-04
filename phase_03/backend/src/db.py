"""Database configuration and session management."""

from sqlmodel import create_engine, Session, SQLModel
import os
from typing import Generator

# Get database URL from environment variable
# Default to SQLite for local development if not set, or if set to a generic placeholder
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app_local.db")

# For Neon (serverless Postgres), we need to ensure we use the correct driver
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
elif DATABASE_URL and "?sslmode=require" in DATABASE_URL:
    # For PostgreSQL connections, ensure psycopg2 compatibility
    if "postgresql://" in DATABASE_URL:
        # Add psycopg2 driver if not present
        if "+psycopg2" not in DATABASE_URL:
            DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# Handle environment-specific configurations
# If explicitly in development or using local SQLite
if os.getenv("ENVIRONMENT") == "development" or "sqlite" in DATABASE_URL:
    if "sqlite" not in DATABASE_URL:
         DATABASE_URL = "sqlite:///./todo_app_local.db"

# Create SQLModel engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for debugging SQL queries
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session

def init_db():
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)