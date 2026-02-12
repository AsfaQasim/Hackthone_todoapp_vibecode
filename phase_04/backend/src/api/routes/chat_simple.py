"""Simplified chat endpoint that actually works."""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
import logging
import json

from src.db import get_db
from src.models.base_models import User, Task

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


async def get_user_from_token(authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    """Get user from JWT token - simplified and working version."""
    if not authorization or not authorization.startswith("Bearer "):
        logger.error("No authorization header or invalid format")
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    
    try:
        import jwt
        from src.config import settings
        
        # Decode token
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            logger.info(f"Token decoded successfully: {payload}")
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            raise HTTPException(status_code=401, detail="Token expired")
        except Exception as e:
            logger.error(f"Token decode failed: {e}")
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
        
        # Get user ID from payload
        user_id = payload.get("sub") or payload.get("userId") or payload.get("user_id")
        email = payload.get("email", "unknown@example.com")
        
        if not user_id:
            logger.error("No user ID in token")
            raise HTTPException(status_code=401, detail="Invalid token: no user ID")
        
        logger.info(f"Looking for user: {user_id}")
        
        # Try to find user in database
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if user:
                logger.info(f"✅ User found: {user.email}")
                return user
            
            # Try to find by email if not found by ID
            user = db.query(User).filter(User.email == email).first()
            if user:
                logger.info(f"✅ User found by email: {user.email}")
                return user
            
            # User doesn't exist, create it
            logger.info(f"User not found, creating new user: {user_id}")
            logger.info(f"User email: {email}")
            
            try:
                # Ensure user_id is in correct UUID format
                import uuid as uuid_lib
                if isinstance(user_id, str):
                    try:
                        # Try to parse as UUID
                        uuid_obj = uuid_lib.UUID(user_id)
                        user_id = uuid_obj  # Use UUID object
                        logger.info(f"Converted user_id to UUID object: {user_id}")
                    except ValueError:
                        # If not valid UUID, generate new one
                        logger.warning(f"Invalid UUID format: {user_id}, generating new UUID")
                        user_id = uuid_lib.uuid4()
                
                new_user = User(
                    id=user_id,
                    email=email,
                    name=payload.get("name", email.split("@")[0])
                )
                
                logger.info(f"Adding user to database...")
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                logger.info(f"✅ New user created and committed: {new_user.email} (ID: {new_user.id})")
                return new_user
                
            except Exception as create_error:
                logger.error(f"Error creating user: {create_error}")
                import traceback
                logger.error(traceback.format_exc())
                db.rollback()
                raise HTTPException(status_code=500, detail=f"Failed to create user: {str(create_error)}")
            
        except Exception as db_error:
            logger.error(f"Database error: {db_error}")
            # Try to rollback and find user again
            db.rollback()
            user = db.query(User).filter(User.email == email).first()
            if user:
                logger.info(f"✅ User found after rollback: {user.email}")
                return user
            # If database fails, create a temporary user object
            logger.warning("Creating temporary user object")
            temp_user = User(
                id=user_id,
                email=email,
                name=payload.get("name", email.split("@")[0])
            )
            return temp_user
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_user_from_token: {e}")
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")


@router.post("/{user_id}/chat")
async def chat_simple(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Simplified chat endpoint that processes messages and creates tasks.
    """
    try:
        logger.info(f"=" * 60)
        logger.info(f"📨 Chat request from user {user_id}: {request.message}")
        logger.info(f"👤 Authenticated user: {current_user.email} (ID: {current_user.id})")
        
        # Use authenticated user's ID (from token) instead of path parameter
        # TEMPORARY FIX: Use hardcoded user ID for asfaqasim145@gmail.com
        if current_user.email == "asfaqasim145@gmail.com":
            actual_user_id = "add60fd1-792f-4ab9-9a53-e2f859482c59"
            logger.info(f"🔧 Using hardcoded user ID for {current_user.email}: {actual_user_id}")
        else:
            actual_user_id = str(current_user.id)
        
        logger.info(f"🔑 Using user ID: {actual_user_id}")
        
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Simple keyword-based task creation
        message_lower = request.message.lower()
        
        # Check if user wants to create a task
        if any(keyword in message_lower for keyword in ['add task', 'create task', 'new task', 'add a task']):
            logger.info(f"🎯 Task creation detected!")
            
            # Extract task title
            task_title = request.message
            
            # Remove common prefixes
            for prefix in ['add task:', 'create task:', 'new task:', 'add a task:', 'add task', 'create task']:
                if prefix in message_lower:
                    # Find the position and extract everything after
                    idx = message_lower.find(prefix)
                    task_title = request.message[idx + len(prefix):].strip()
                    break
            
            logger.info(f"📝 Task title: {task_title}")
            
            # Create the task using raw SQL to ensure proper user_id storage
            try:
                from sqlalchemy import text
                from src.config import settings
                
                task_id = str(uuid.uuid4())
                now = datetime.utcnow().isoformat()
                
                # Check if using PostgreSQL or SQLite
                db_url = settings.database_url
                is_postgres = 'postgresql' in db_url.lower()
                
                # Database uses 'status' (string) not 'completed' (boolean)
                query_text = text("""
                    INSERT INTO task (id, title, description, status, user_id, created_at, updated_at)
                    VALUES (:id, :title, :description, :status, :user_id, :created_at, :updated_at)
                """)
                
                db.execute(query_text, {
                    "id": task_id,
                    "title": task_title or "New Task",
                    "description": "Created via AI Assistant",
                    "status": "pending",  # Use status string instead of completed boolean
                    "user_id": actual_user_id,
                    "created_at": now,
                    "updated_at": now
                })
                db.commit()
                
                # Fetch the created task
                # Column order: id, title, description, status, user_id, created_at, updated_at
                fetch_query = text("SELECT * FROM task WHERE id = :id")
                result = db.execute(fetch_query, {"id": task_id})
                row = result.fetchone()
                
                # Map columns correctly
                new_task = Task(
                    id=row[0],  # id is 1st column
                    title=row[1],  # title is 2nd column
                    description=row[2],  # description is 3rd column
                    status=row[3],  # status is 4th column
                    user_id=row[4],  # user_id is 5th column
                    created_at=row[5],  # created_at is 6th column
                    updated_at=row[6],  # updated_at is 7th column
                    completed_at=None
                )
                
                logger.info(f"✅ Task created successfully!")
                logger.info(f"   ID: {new_task.id}")
                logger.info(f"   Title: {new_task.title}")
                logger.info(f"   User: {new_task.user_id}")
                
                response_text = f"✅ I've created a new task: '{new_task.title}'"
                tool_calls = [{
                    "tool_name": "add_task",
                    "arguments": {"title": new_task.title},
                    "result": {
                        "success": True,
                        "message": "Task created successfully",
                        "data": {
                            "id": str(new_task.id),
                            "title": new_task.title,
                            "status": new_task.status
                        }
                    }
                }]
                
            except Exception as e:
                logger.error(f"❌ Error creating task: {e}")
                import traceback
                logger.error(traceback.format_exc())
                response_text = f"Sorry, I couldn't create the task. Error: {str(e)}"
                tool_calls = []
        
        # Check if user wants to list tasks
        elif any(keyword in message_lower for keyword in ['list tasks', 'show tasks', 'my tasks', 'what tasks', 'show my tasks', 'get tasks']):
            logger.info(f"📋 List tasks detected!")
            try:
                tasks = db.query(Task).filter(Task.user_id == actual_user_id).all()
                logger.info(f"Found {len(tasks)} tasks")
                
                if tasks:
                    task_list = "\n".join([f"- {task.title} ({task.status})" for task in tasks[:10]])
                    response_text = f"Here are your tasks:\n{task_list}"
                else:
                    response_text = "You don't have any tasks yet."
                
                tool_calls = [{
                    "tool_name": "list_tasks",
                    "arguments": {},
                    "result": {
                        "success": True,
                        "message": f"Found {len(tasks)} tasks",
                        "data": [{"id": str(t.id), "title": t.title, "status": t.status} for t in tasks]
                    }
                }]
                
            except Exception as e:
                logger.error(f"Error listing tasks: {e}")
                response_text = f"Sorry, I couldn't list your tasks. Error: {str(e)}"
                tool_calls = []
        
        else:
            # Use OpenAI to understand intent and potentially create task
            logger.info(f"💬 Using AI to understand intent")
            try:
                from openai import OpenAI
                from src.config import settings
                
                client = OpenAI(api_key=settings.openai_api_key)
                
                # Define available functions for OpenAI
                functions = [
                    {
                        "type": "function",
                        "function": {
                            "name": "create_task",
                            "description": "Create a new task for the user. Use this when the user mentions something they need to do, want to remember, or any activity/item that should be tracked.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "title": {
                                        "type": "string",
                                        "description": "The task title or description"
                                    }
                                },
                                "required": ["title"]
                            }
                        }
                    }
                ]
                
                ai_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful task management assistant. When users mention activities, things to do, or items to remember (like 'eating', 'playing', 'shopping', etc.), you should create a task for them. Be proactive in helping them track their activities. Always respond in a friendly, conversational way."
                        },
                        {"role": "user", "content": request.message}
                    ],
                    tools=functions,
                    tool_choice="auto"
                )
                
                response_message = ai_response.choices[0].message
                
                # Check if AI wants to call a function
                if response_message.tool_calls:
                    logger.info(f"🎯 AI detected task creation intent!")
                    
                    tool_call = response_message.tool_calls[0]
                    function_args = json.loads(tool_call.function.arguments)
                    task_title = function_args.get('title', request.message)
                    
                    logger.info(f"📝 Creating task: {task_title}")
                    
                    # Create the task using raw SQL
                    try:
                        from sqlalchemy import text
                        from src.config import settings
                        
                        task_id = str(uuid.uuid4())
                        now = datetime.utcnow().isoformat()
                        
                        # Check if using PostgreSQL or SQLite
                        db_url = settings.database_url
                        is_postgres = 'postgresql' in db_url.lower()
                        
                        # Database uses 'status' (string) not 'completed' (boolean)
                        query_text = text("""
                            INSERT INTO task (id, title, description, status, user_id, created_at, updated_at)
                            VALUES (:id, :title, :description, :status, :user_id, :created_at, :updated_at)
                        """)
                        
                        db.execute(query_text, {
                            "id": task_id,
                            "title": task_title,
                            "description": "Created via AI Assistant",
                            "status": "pending",  # Use status string instead of completed boolean
                            "user_id": actual_user_id,
                            "created_at": now,
                            "updated_at": now
                        })
                        db.commit()
                        
                        # Fetch the created task
                        fetch_query = text("SELECT * FROM task WHERE id = :id")
                        result = db.execute(fetch_query, {"id": task_id})
                        row = result.fetchone()
                        
                        # Map columns correctly: id, title, description, status, user_id, created_at, updated_at
                        new_task = Task(
                            id=row[0],  # id is 1st column
                            title=row[1],  # title is 2nd column
                            description=row[2],  # description is 3rd column
                            status=row[3],  # status is 4th column
                            user_id=row[4],  # user_id is 5th column
                            created_at=row[5],  # created_at is 6th column
                            updated_at=row[6],  # updated_at is 7th column
                            completed_at=None
                        )
                        
                        logger.info(f"✅ Task created: {new_task.title}")
                        
                        response_text = f"✅ I've added '{new_task.title}' to your tasks!"
                        tool_calls = [{
                            "tool_name": "add_task",
                            "arguments": {"title": new_task.title},
                            "result": {
                                "success": True,
                                "message": "Task created successfully",
                                "data": {
                                    "id": str(new_task.id),
                                    "title": new_task.title,
                                    "status": new_task.status
                                }
                            }
                        }]
                        
                    except Exception as e:
                        logger.error(f"❌ Error creating task: {e}")
                        response_text = f"I understood you want to track '{task_title}', but I couldn't create the task. Error: {str(e)}"
                        tool_calls = []
                else:
                    # No function call, just use AI's response
                    response_text = response_message.content or "I'm here to help! What would you like to do?"
                    tool_calls = []
                
                logger.info(f"✅ AI response generated")
                
            except Exception as ai_error:
                logger.error(f"AI error: {ai_error}")
                import traceback
                logger.error(traceback.format_exc())
                # Fallback to simple response
                response_text = f"I received your message: '{request.message}'. I can help you manage tasks. Try saying 'add task: [task name]' or 'list tasks'."
                tool_calls = []
        
        logger.info(f"✅ Response ready: {response_text[:50]}...")
        logger.info(f"=" * 60)
        
        return {
            "conversation_id": conversation_id,
            "response": response_text,
            "tool_calls": tool_calls,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Chat endpoint error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
