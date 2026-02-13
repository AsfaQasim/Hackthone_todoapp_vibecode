"""Check if there are any tasks in the database."""
import sys
import os
sys.path.insert(0, 'backend')
sys.path.insert(0, 'backend/src')

from sqlmodel import Session, select
from src.db import engine
from src.models.base_models import Task, User

print("Checking database for tasks...")
print("=" * 70)

with Session(engine) as session:
    # Check users
    users = session.exec(select(User)).all()
    print(f"\n📊 Total users: {len(users)}")
    for user in users:
        print(f"  - {user.email} (ID: {user.id})")
    
    # Check tasks
    tasks = session.exec(select(Task)).all()
    print(f"\n📋 Total tasks: {len(tasks)}")
    
    if tasks:
        for task in tasks:
            print(f"\n  Task: {task.title}")
            print(f"    ID: {task.id}")
            print(f"    User ID: {task.user_id}")
            print(f"    Status: {task.status}")
            print(f"    Description: {task.description}")
    else:
        print("\n  ❌ No tasks found in database!")
        print("\n  You need to create tasks using:")
        print("    1. AI Assistant at http://localhost:3000/chat")
        print("    2. Or manually at http://localhost:3000/tasks")

print("\n" + "=" * 70)
