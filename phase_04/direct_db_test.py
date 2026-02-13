#!/usr/bin/env python3
"""Direct test of the task creation and retrieval logic."""

import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / "src"))

# Change to backend directory so config can be imported
original_cwd = os.getcwd()
os.chdir(str(backend_path))

from src.db import engine, init_db
from src.models.base_models import Task, User, TaskStatus
from sqlmodel import Session, select
import uuid
from datetime import datetime

def test_task_creation_retrieval():
    """Test task creation and retrieval directly through the database."""
    print("=" * 80)
    print("DIRECT DATABASE TEST")
    print("=" * 80)
    
    try:
        # Initialize database
        init_db()
        print("Database initialized successfully")
        
        # Create a test user
        with Session(engine) as session:
            # Check if test user already exists
            test_user = session.exec(select(User).where(User.email == "test@example.com")).first()
            
            if not test_user:
                # Create a new test user
                test_user = User(email="test@example.com", name="Test User")
                session.add(test_user)
                session.commit()
                session.refresh(test_user)
                print(f"Created test user: {test_user.email} (ID: {test_user.id})")
            else:
                print(f"Found existing test user: {test_user.email} (ID: {test_user.id})")
        
        # Create a task for the user
        with Session(engine) as session:
            new_task = Task(
                title="Test task from direct database test",
                description="Created during direct database test",
                status=TaskStatus.PENDING,
                user_id=str(test_user.id)
            )
            
            session.add(new_task)
            session.commit()
            session.refresh(new_task)
            
            print(f"Created task: {new_task.title} (ID: {new_task.id})")
        
        # Retrieve tasks for the user
        with Session(engine) as session:
            # Get all tasks for this user
            user_tasks = session.exec(select(Task).where(Task.user_id == str(test_user.id))).all()
            print(f"Retrieved {len(user_tasks)} tasks for user")
            
            for i, task in enumerate(user_tasks):
                print(f"  {i+1}. {task.title} - Status: {task.status}")
        
        # Test with raw SQL to mimic what the API does
        with Session(engine) as session:
            from sqlalchemy import text
            
            # Raw SQL query like in the API
            query_text = text("SELECT * FROM task WHERE user_id = :user_id")
            result = session.execute(query_text, {"user_id": str(test_user.id)})
            rows = result.fetchall()
            
            print(f"Raw SQL found {len(rows)} tasks for user")
            
            for i, row in enumerate(rows):
                # Based on our schema: 0:title, 1:description, 2:status, 3:id, 4:user_id, 5:created_at, 6:updated_at, 7:completed_at
                print(f"  {i+1}. Title: {row[0]}, Status: {row[2]}, ID: {row[3]}")
        
        print("\nDirect database test completed successfully!")
        
    except Exception as e:
        print(f"Direct database test failed: {e}")
        import traceback
        traceback.print_exc()


def test_user_task_mapping():
    """Test that user ID mapping works correctly."""
    print("\n" + "=" * 80)
    print("USER-TASK MAPPING TEST")
    print("=" * 80)
    
    try:
        with Session(engine) as session:
            # Create multiple users
            user1 = session.exec(select(User).where(User.email == "user1@example.com")).first()
            if not user1:
                user1 = User(email="user1@example.com", name="User 1")
                session.add(user1)
                session.commit()
                session.refresh(user1)
            
            user2 = session.exec(select(User).where(User.email == "user2@example.com")).first()
            if not user2:
                user2 = User(email="user2@example.com", name="User 2")
                session.add(user2)
                session.commit()
                session.refresh(user2)
            
            print(f"Created/Found users: {user1.email}, {user2.email}")
            
            # Create tasks for each user
            task1 = Task(title="User 1 task", description="Task for user 1", status=TaskStatus.PENDING, user_id=str(user1.id))
            task2 = Task(title="Another user 1 task", description="Another task for user 1", status=TaskStatus.COMPLETED, user_id=str(user1.id))
            task3 = Task(title="User 2 task", description="Task for user 2", status=TaskStatus.PENDING, user_id=str(user2.id))
            
            session.add(task1)
            session.add(task2)
            session.add(task3)
            session.commit()
            
            print(f"Created 3 tasks: 2 for user1, 1 for user2")
            
            # Test retrieval for user1
            user1_tasks = session.exec(select(Task).where(Task.user_id == str(user1.id))).all()
            print(f"User 1 has {len(user1_tasks)} tasks")
            
            # Test retrieval for user2
            user2_tasks = session.exec(select(Task).where(Task.user_id == str(user2.id))).all()
            print(f"User 2 has {len(user2_tasks)} tasks")
            
            # Verify no cross-contamination
            all_tasks = session.exec(select(Task)).all()
            print(f"Total tasks in database: {len(all_tasks)}")
            
    except Exception as e:
        print(f"User-task mapping test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_task_creation_retrieval()
    test_user_task_mapping()
    
    # Change back to original directory
    os.chdir(original_cwd)