"""Check tasks in database"""
import sys
import os
sys.path.insert(0, 'backend')
sys.path.insert(0, 'backend/src')

from db import SessionLocal
from models.base_models import Task, User

db = SessionLocal()

print("All Users:")
users = db.query(User).all()
for user in users:
    print(f"  - {user.id} ({user.email})")

print("\nAll Tasks:")
tasks = db.query(Task).all()
for task in tasks:
    print(f"  - {task.id} | User: {task.user_id} | Title: {task.title}")

db.close()
