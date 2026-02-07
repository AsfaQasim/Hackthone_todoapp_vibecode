"""Database utilities and session management for the AI Chatbot with MCP application."""

from typing import Generator
from sqlmodel import create_engine, Session, SQLModel
from config import settings
import os
# db
# Create the database engine with proper configuration
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = settings.database_url

# Fix postgres scheme for SQLAlchemy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session

def init_db():
    """Initialize the database tables."""
    from src.models.base_models import User, Task, Conversation, Message
    import logging

    logger = logging.getLogger(__name__)

    try:
        # Import all models here to ensure they're registered with SQLModel
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        # If there's a schema mismatch, we may need to recreate tables
        # This is a simplified approach - in production, use Alembic for migrations
        try:
            from sqlalchemy import inspect
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()

            if existing_tables:  # If there are existing tables
                logger.warning("Existing tables found, attempting to recreate with correct schema...")
                # Close all connections before dropping
                engine.dispose()

                # Recreate engine to ensure fresh connection
                temp_engine = create_engine(
                    DATABASE_URL,
                    echo=False,
                    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
                )

                # Drop all tables and recreate
                SQLModel.metadata.drop_all(temp_engine)
                SQLModel.metadata.create_all(temp_engine)

                # Close temp engine
                temp_engine.dispose()
                logger.info("Database tables recreated successfully")
            else:
                # If no existing tables, just try creating them again
                SQLModel.metadata.create_all(engine)
        except Exception as e2:
            logger.error(f"Failed to fix database schema: {e2}")
            raise
