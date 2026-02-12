# Backend Guidelines

## Stack
- FastAPI
- SQLModel (ORM)
- Neon PostgreSQL
- Better Auth (JWT verification)

## Project Structure
- `main.py` - FastAPI app entry point
- `models.py` - SQLModel database models
- `routes/` - API route handlers
- `db.py` - Database connection
- `auth.py` - Authentication middleware/utils

## API Conventions
- All routes under `/api/`
- Return JSON responses
- Use Pydantic models for request/response
- Handle errors with HTTPException
- All endpoints must include JWT token verification

## Database
- Use SQLModel for all database operations
- Connection string from environment variable: DATABASE_URL

## Running
`uvicorn main:app --reload --port 8000`
