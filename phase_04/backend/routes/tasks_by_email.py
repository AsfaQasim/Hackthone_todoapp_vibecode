"""Simple tasks endpoint that fetches by email"""
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlalchemy import text
from src.db import get_db
import logging

router = APIRouter(prefix="/api", tags=["tasks-by-email"])
logger = logging.getLogger(__name__)


@router.get("/my-tasks")
def get_my_tasks(session: Session = Depends(get_db)):
    """
    Get all tasks for asfaqasim145@gmail.com
    Simple endpoint that doesn't require authentication
    """
    try:
        email = "asfaqasim145@gmail.com"
        
        logger.info(f"=" * 60)
        logger.info(f"📋 Fetching tasks for: {email}")
        
        # Get user ID from email
        user_query = text('SELECT id FROM "user" WHERE email = :email')
        user_result = session.execute(user_query, {"email": email})
        user_row = user_result.fetchone()
        
        if not user_row:
            logger.warning(f"User not found: {email}")
            return []
        
        user_id = str(user_row[0])
        logger.info(f"Found user ID: {user_id}")
        
        # Get all tasks for this user
        # Column order: title, description, completed, user_id, id, created_at, updated_at
        tasks_query = text("SELECT * FROM task WHERE user_id = :user_id ORDER BY created_at DESC")
        result = session.execute(tasks_query, {"user_id": user_id})
        
        tasks = []
        for row in result:
            # Column order: title, description, completed, user_id, id, created_at, updated_at
            task = {
                "id": str(row[4]),  # id is 5th column
                "title": row[0],  # title is 1st column
                "description": row[1],  # description is 2nd column
                "status": "completed" if row[2] else "pending",  # completed is 3rd column (boolean)
                "user_id": str(row[3]),  # user_id is 4th column
                "created_at": row[5].isoformat() if row[5] else None,  # created_at is 6th
                "updated_at": row[6].isoformat() if row[6] else None,  # updated_at is 7th
                "completed_at": None
            }
            tasks.append(task)
        
        logger.info(f"✅ Found {len(tasks)} tasks")
        for task in tasks:
            logger.info(f"  - {task['title']} (ID: {task['id'][:8]}...)")
        logger.info(f"=" * 60)
        
        return tasks
        
    except Exception as e:
        logger.error(f"❌ Error fetching tasks: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
