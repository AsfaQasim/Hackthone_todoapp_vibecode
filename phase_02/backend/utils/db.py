from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL - using Neon Serverless PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please check your .env file.")

# Create engine with optimized settings for Neon serverless
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for debugging SQL queries in development
    pool_size=5,  # Small pool for serverless
    max_overflow=10,  # Allow some overflow
    pool_pre_ping=True,  # Verify connections before use (essential for Neon)
    pool_recycle=300,  # Recycle connections every 5 minutes
    pool_timeout=30,  # 30 seconds to get connection from pool
    connect_args={
        "connect_timeout": 30,  # 30 second timeout for connection
        "application_name": "todo-app",  # Helps with Neon connection tracking
        "options": "-c statement_timeout=30000"  # 30 second statement timeout
    }
)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session