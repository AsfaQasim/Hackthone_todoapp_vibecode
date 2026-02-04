import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.config import settings

print("DATABASE_URL from settings:", settings.database_url)
print("DATABASE_URL from os.environ:", os.environ.get("DATABASE_URL", "Not set"))

# Also test the engine creation
from sqlalchemy import create_engine
db_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
print("Using database URL:", db_url)
engine = create_engine(db_url)
print("Engine dialect:", engine.dialect.name)