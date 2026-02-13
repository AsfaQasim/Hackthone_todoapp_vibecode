#!/usr/bin/env python3
"""Debug script to test the tasks endpoint and identify the issue."""

import os
import sys
from pathlib import Path
import requests
import json
import uuid

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / "src"))

# Change to backend directory so config can be imported
original_cwd = os.getcwd()
os.chdir(str(backend_path))

from src.db import engine, init_db
from sqlalchemy import text
from src.models.base_models import Task, User, TaskStatus
from sqlmodel import Session, select

def test_database_connection():
    """Test database connection and check for tasks."""
    print("=" * 80)
    print("TESTING DATABASE CONNECTION")
    print("=" * 80)
    
    try:
        # Initialize database
        init_db()
        print("Database initialized successfully")
        
        # Connect to database
        with Session(engine) as session:
            # Count users
            user_count = session.exec(select(User)).all()
            print(f"Users in database: {len(user_count)}")
            
            # Count tasks
            task_count = session.exec(select(Task)).all()
            print(f"Tasks in database: {len(task_count)}")
            
            if task_count:
                print("\nSample tasks:")
                for i, task in enumerate(task_count[:3]):  # Show first 3 tasks
                    print(f"  {i+1}. ID: {task.id}")
                    print(f"     Title: {task.title}")
                    print(f"     Status: {task.status}")
                    print(f"     User ID: {task.user_id}")
                    print(f"     Created: {task.created_at}")
                    print()
            
            # Check for any user
            if user_count:
                sample_user = user_count[0]
                print(f"Sample user: {sample_user.email} (ID: {sample_user.id})")
                
                # Check tasks for this user
                user_tasks = session.exec(select(Task).where(Task.user_id == str(sample_user.id))).all()
                print(f"Tasks for this user: {len(user_tasks)}")
                
    except Exception as e:
        print(f"Database test failed: {e}")
        import traceback
        traceback.print_exc()


def test_backend_endpoints():
    """Test backend endpoints directly."""
    print("\n" + "=" * 80)
    print("TESTING BACKEND ENDPOINTS")
    print("=" * 80)
    
    # Try to get a valid token by creating a test user programmatically
    try:
        from src.services.auth_service import create_access_token
        from src.db import get_db
        
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
                print(f"Created test user: {test_user.email}")
            else:
                print(f"Found existing test user: {test_user.email}")
        
        # Create a token for the test user
        token_payload = {
            "sub": str(test_user.id),
            "email": test_user.email,
            "name": test_user.name
        }
        token = create_access_token(token_payload)
        print(f"Generated test token: {token[:30]}...")
        
        # Test the tasks endpoint
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print(f"\nTesting GET /api/tasks endpoint...")
        response = requests.get("http://localhost:8000/api/tasks", headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"Successfully fetched {len(tasks)} tasks")
            for i, task in enumerate(tasks[:3]):
                print(f"  {i+1}. {task.get('title', 'No title')} - {task.get('status', 'No status')}")
        else:
            print(f"Failed to fetch tasks: {response.text}")
        
        # Test creating a task
        print(f"\nTesting POST /api/tasks endpoint...")
        new_task_data = {
            "title": "Test task from debug script",
            "description": "Created during debugging"
        }
        response = requests.post(
            "http://localhost:8000/api/tasks", 
            headers=headers, 
            json=new_task_data
        )
        print(f"Create task response status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            created_task = response.json()
            print(f"Created task: {created_task.get('title', 'Unknown')}")
        else:
            print(f"Failed to create task: {response.text}")
            
    except Exception as e:
        print(f"Endpoint test failed: {e}")
        import traceback
        traceback.print_exc()


def check_route_conflicts():
    """Check for route conflicts."""
    print("\n" + "=" * 80)
    print("CHECKING FOR ROUTE CONFLICTS")
    print("=" * 80)
    
    try:
        from main import app
        routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                routes.append({
                    'path': route.path,
                    'methods': list(route.methods) if isinstance(route.methods, set) else route.methods
                })
        
        print("Registered routes:")
        for route in sorted(routes, key=lambda x: x['path']):
            print(f"  {route['methods']} {route['path']}")
        
        # Check for conflicting routes
        api_routes = [r for r in routes if '/api' in r['path']]
        print(f"\nAPI routes found: {len(api_routes)}")
        
        # Look for potential conflicts
        tasks_routes = [r for r in api_routes if 'tasks' in r['path']]
        print(f"Tasks-related routes: {len(tasks_routes)}")
        for route in tasks_routes:
            print(f"  {route['methods']} {route['path']}")
            
    except Exception as e:
        print(f"Route check failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_database_connection()
    test_backend_endpoints()
    check_route_conflicts()
    
    # Change back to original directory
    os.chdir(original_cwd)