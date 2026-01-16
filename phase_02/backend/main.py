from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Todo API",
    description="Secure Todo API with JWT authentication and user isolation",
    version="1.0.0"
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Next.js development server
        "http://127.0.0.1:3000",      # Alternative localhost
        "http://localhost:3001",      # Alternative Next.js port
        "http://127.0.0.1:3001",      # Alternative localhost
        # Add your production domain when deploying
    ],
    allow_credentials=True,
    allow_methods=["*"],              # In production, specify only required methods
    allow_headers=["*"],              # In production, specify only required headers
)

def warm_up_database():
    """Warm up the database connection to minimize Neon cold-start issues"""
    try:
        # Import here to avoid circular imports
        from utils.db import get_session
        from models.todo_models import User
        from sqlmodel import select
        
        # Create a simple database session to establish connection
        for db in get_session():
            # Execute a simple query to warm up the connection
            db.execute(select(User).limit(1))
            break  # Only need to execute once
        print("✅ Database connection warmed up successfully")
    except Exception as e:
        print(f"⚠️ Database warm-up failed: {e}")
        print("This might be normal if no users exist yet")

@app.on_event("startup")
def startup_event():
    """Initialize database and warm up connections on startup"""
    # Create database tables
    from sqlmodel import SQLModel
    from utils.db import engine
    SQLModel.metadata.create_all(bind=engine)
    
    # Warm up database connection
    warm_up_database()
    
    print("🚀 Todo API started successfully")

# Include your routers after CORS configuration
from api.auth_routes import router as auth_router
from api.task_routes import router as task_router

app.include_router(auth_router)
app.include_router(task_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Todo API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)