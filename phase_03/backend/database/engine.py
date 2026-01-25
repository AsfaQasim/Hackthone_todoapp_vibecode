from sqlmodel import SQLModel, create_engine
from sqlmodel import Session
import os

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """
    Create database tables based on SQLModel models
    """
    SQLModel.metadata.create_all(engine)


def get_db():
    """
    Generator function to get database session
    Used as a FastAPI dependency
    """
    with Session(engine) as session:
        yield session