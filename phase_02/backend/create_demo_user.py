"""
Script to initialize a default user in your database for testing purposes.
"""
import sys
import os
from sqlmodel import Session, select
from utils.db import engine
from models.user_model import User
from api.user_service import create_user_in_db
from schemas.user_schema import UserCreate
import hashlib

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
        
        user = create_user_in_db(session, user_data)
        print(f"Demo user created successfully!")
        print(f"User ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Password: demo123")
        print("\nYou can now use these credentials to log in.")

if __name__ == "__main__":
    create_default_user()