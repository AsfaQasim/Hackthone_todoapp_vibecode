from src.db import engine, init_db
from src.models.base_models import User, Task, Conversation, Message
from sqlmodel import Session, select
import sys

try:
    print("Checking database initialization...")
    init_db()
    print("Database initialized successfully.")
    
    print("Checking model imports...")
    with Session(engine) as session:
        print("Session created successfully.")
        
    print("Backend check passed!")
except Exception as e:
    print(f"Backend check failed: {e}")
    sys.exit(1)
