from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
load_dotenv()

from middleware.auth_middleware import JWTBearer, verify_user_is_authenticated
from routes import auth, tasks, todos

 # Import the todos, auth, and tasks routers
from database.engine import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler to validate required environment variables on startup
    and initialize database tables
    """
    # Check if BETTER_AUTH_SECRET is set
    if not os.getenv("BETTER_AUTH_SECRET"):
        raise RuntimeError(
            "BETTER_AUTH_SECRET environment variable is not set.\n"
            "Please set BETTER_AUTH_SECRET for production use.\n"
            "For development, add 'BETTER_AUTH_SECRET=dev_secret_for_testing_only' to your environment."
        )

    # Initialize database tables
    print("Initializing database tables...")
    create_db_and_tables()
    print("Database tables initialized successfully.")

    yield

    # Cleanup on shutdown if needed
    print("Shutting down...")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Todo API with JWT Authentication",
    description="Secure Todo API with Better Auth JWT integration",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js default development server
        "http://localhost:3001",  # Alternative Next.js port
        "https://yourdomain.com"   # Production domain - replace with actual domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(todos.router, prefix="/todos", tags=["todos"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])  # Tasks API with prefixed routes


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API with JWT Authentication"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-api"}


# Protected endpoint example - requires authentication
@app.get("/profile", dependencies=[Depends(JWTBearer())])
def get_profile(current_user=Depends(verify_user_is_authenticated)):
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "message": "Profile accessed successfully"
    }


# Global exception handler for unauthorized access
@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauthorized_exception_handler(request, exc):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized: Invalid or missing authentication token"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )