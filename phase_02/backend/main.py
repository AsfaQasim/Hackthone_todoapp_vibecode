from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from utils.jwt_handler import require_auth, TokenData
from api.todos import router as todos_router
from api.task_routes import router as task_router
from utils.init_db import create_db_and_tables

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Todo API",
    description="Secure Todo API with JWT authentication and user isolation",
    version="1.0.0"
)

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include todo routes
app.include_router(todos_router)
# Include task routes (Spec 2)
app.include_router(task_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Todo API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)