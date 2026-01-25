"""
This script creates a default user in your database for testing purposes.
Run this script to add a demo user with credentials:
Email: demo@example.com
Password: demo123
"""

import sys
import os
import hashlib
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.user import User  # Adjust the import based on your actual model location
from backend.utils.db import Base  # Adjust the import based on your actual DB setup

# Use the same database URL as your application
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_ncA3kGXux5ZQ@ep-holy-flower-ahrkffp6-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_demo_user():
    db = SessionLocal()
    
    # Check if demo user already exists
    existing_user = db.query(User).filter(User.email == "demo@example.com").first()
    
    if existing_user:
        print("Demo user already exists!")
        return
    
    # Create a hashed password (using a simple hash for demo purposes)
    # In a real application, use proper password hashing like bcrypt
    password_hash = hashlib.sha256("demo123".encode()).hexdigest()
    
    # Create the demo user
    demo_user = User(
        email="demo@example.com",
        name="Demo User",
        password=password_hash  # In a real app, use proper hashing
    )
    
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)
    
    print(f"Demo user created successfully with ID: {demo_user.id}")
    print("Credentials:")
    print("Email: demo@example.com")
    print("Password: demo123")

if __name__ == "__main__":
    create_demo_user()