# Backend Guidelines
  
## Stack 
- FastAPI 
- SQLModel (ORM) 
- Neon PostgreSQL 
  
## Project Structure 
- `main.py` - FastAPI app entry point 
- `models.py` - SQLModel database models 
- `routes/` - API route handlers 
- `db.py` - Database connection 
- `auth.py` - Authentication utilities
  
## API Conventions 
- All routes under `/api/` 
- Return JSON responses 
- Use Pydantic models for request/response 
- Handle errors with HTTPException 
  
## Database 
- Use SQLModel for all database operations 
- Connection string from environment variable: DATABASE_URL 
  
## Authentication 
- Verify JWT tokens using shared secret (BETTER_AUTH_SECRET)
- Extract user info from JWT claims
- Ensure user isolation on all operations
- Return 401 for invalid tokens, 403 for unauthorized access
  
## Running 
uvicorn main:app --reload --port 8000