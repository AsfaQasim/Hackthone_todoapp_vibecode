"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")

# Handle environment-specific configurations here
if not os.getenv("ENVIRONMENT") or os.getenv("ENVIRONMENT") == "development":
    # Check if it's the default PostgreSQL URL or the production Neon URL
    if "neon.tech" in DATABASE_URL or "postgresql" in DATABASE_URL:
        DATABASE_URL = "sqlite:///./todo_app_local.db"

# For synchronous operations (needed for Alembic migrations)
SYNC_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "") if "+asyncpg" in DATABASE_URL else DATABASE_URL

engine = create_engine(
    SYNC_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()