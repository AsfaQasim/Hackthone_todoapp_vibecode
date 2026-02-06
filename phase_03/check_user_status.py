"""Check the current user status and tasks in the database."""

import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
sys.path.insert(0, os.path.join(backend_path, 'src'))

from sqlmodel import Session, select
from db import engine
from models.base_models import User, Task

def main():
    """Check user and task status."""
    print("=" * 60)
    print("CHECKING DATABASE STATUS")
    print("=" * 60)
    
    with Session(engine) as session:
        # Get all users
        print("\n1. Users in database:")
        users = session.exec(select(User)).all()
        print(f"   Total users: {len(users)}")
        
        for user in users:
            print(f"\n   User: {user.email}")
            print(f"   ID: {user.id}")
            
            # Get tasks for this user
            tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()
            print(f"   Tasks: {len(tasks)}")
            
            if tasks:
                print(f"   Recent tasks:")
                for task in tasks[:5]:
                    print(f"     - {task.title} ({task.status})")
    
    print("\n" + "=" * 60)
    print("✅ Database check complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
