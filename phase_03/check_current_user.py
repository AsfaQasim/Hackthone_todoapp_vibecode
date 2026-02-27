"""Check if current user exists in database"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from dotenv import load_dotenv
load_dotenv('backend/.env')

from sqlmodel import Session, select
from src.db import engine
from src.models.base_models import User

print("Checking users in database...")
print("=" * 60)

with Session(engine) as session:
    statement = select(User)
    users = session.exec(statement).all()
    
    print(f"Total users in database: {len(users)}")
    print()
    
    for user in users:
        print(f"User ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Name: {user.name}")
        print(f"Created: {user.created_at}")
        print("-" * 60)
    
    # Check for specific user
    target_user_id = "add60fd1-792f-4ab9-9a53-e2f859482c59"
    print(f"\nLooking for user ID: {target_user_id}")
    
    statement = select(User).where(User.id == target_user_id)
    user = session.exec(statement).first()
    
    if user:
        print(f"✅ User found: {user.email}")
    else:
        print(f"❌ User NOT found in database")
