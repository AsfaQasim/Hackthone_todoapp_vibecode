from sqlmodel import SQLModel
from utils.db import engine
from models.task_model import Task  # Import all models to register them with SQLModel
from models.user_model import User

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
    print("Database tables created successfully!")