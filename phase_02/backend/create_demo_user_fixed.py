"""
Script to initialize a default user in your database for testing purposes.
"""
import sys
import os
# Add the backend directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session, select
from utils.db import engine
from models.user_model import User
from api.user_service import create_user_in_db
from pydantic import BaseModel
import uuid
from datetime import datetime

# Define UserCreate schema here since it might not be in the schemas module
class UserCreate(BaseModel):
    email: str
    name: str
    password: str

def create_default_user():
    # Create a database session
    with Session(engine) as session:
        # Check if the default user already exists
        existing_user = session.exec(select(User).where(User.email == "demo@example.com")).first()
        
        if existing_user:
            print("Demo user already exists!")
            print(f"Email: demo@example.com")
            print(f"Password: demo123")
            return
        
        # Create a new user with default credentials
        user_data = UserCreate(
            email="demo@example.com",
            name="Demo User",
            password="demo123"  # This should be properly hashed in a real application
        )
        
        # Create user directly using User model
        db_user = User(
            email=user_data.email,
            name=user_data.name,
            password=user_data.password  # Should be hashed in real app
        )
        
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        
        print(f"Demo user created successfully!")
        print(f"User ID: {db_user.id}")
        print(f"Email: {db_user.email}")
        print(f"Password: demo123")
        print("\nYou can now use these credentials to log in.")

if __name__ == "__main__":
    create_default_user()