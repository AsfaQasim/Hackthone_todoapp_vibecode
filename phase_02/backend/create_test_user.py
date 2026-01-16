"""
Script to create a test user in your database with a known password.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session
from utils.db import engine
from models.user_model import User
from api.user_service import create_user_in_db
from pydantic import BaseModel
import hashlib
import bcrypt

# Define UserCreate schema here since it might not be in the schemas module
class UserCreate(BaseModel):
    email: str
    name: str
    password: str

def create_test_user():
    # Create a database session
    with Session(engine) as session:
        # Create a new user with test credentials
        test_email = "test@example.com"
        test_password = "password123"  # Plain text for testing
        test_name = "Test User"
        
        # Hash the password using bcrypt (recommended approach)
        hashed_password = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Check if the test user already exists
        from sqlmodel import select
        existing_user = session.exec(select(User).where(User.email == test_email)).first()
        
        if existing_user:
            print(f"Test user {test_email} already exists!")
        else:
            # Create user with hashed password
            user_data = UserCreate(
                email=test_email,
                name=test_name,
                password=hashed_password  # Store hashed password
            )
            
            # Create user directly using User model
            db_user = User(
                email=user_data.email,
                name=user_data.name,
                password=hashed_password  # Store hashed password
            )
            
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            
            print(f"Test user created successfully!")
            print(f"Email: {test_email}")
            print(f"Password: {test_password}")
            print(f"You can now use these credentials to log in.")
        
        # Also create a demo user with simple password
        demo_email = "demo@example.com"
        demo_password = "demo123"
        demo_name = "Demo User"
        
        demo_existing = session.exec(select(User).where(User.email == demo_email)).first()
        
        if demo_existing:
            print(f"Demo user {demo_email} already exists!")
        else:
            demo_hashed_password = bcrypt.hashpw(demo_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            demo_user = User(
                email=demo_email,
                name=demo_name,
                password=demo_hashed_password
            )
            
            session.add(demo_user)
            session.commit()
            session.refresh(demo_user)
            
            print(f"Demo user created successfully!")
            print(f"Email: {demo_email}")
            print(f"Password: {demo_password}")

if __name__ == "__main__":
    create_test_user()