# Todo App Backend - Authentication System

This backend implements a secure, JWT-based authentication system that follows the Better Auth integration specification.

## Architecture Overview

```
Frontend (Next.js + Better Auth) <---> Backend (FastAPI + JWT Verification)
```

The authentication flow works as follows:
1. Frontend handles user authentication via Better Auth
2. Better Auth generates a JWT token
3. Frontend sends JWT token in Authorization header to backend
4. Backend verifies the JWT token using the shared secret
5. Backend extracts user identity from the verified token
6. Backend enforces user isolation by filtering data based on user ID

## Key Components

### 1. JWT Handler (`utils/jwt_handler.py`)
- Creates and verifies JWT tokens
- Uses the same secret key as Better Auth for compatibility
- Enforces token expiration (7 days as per spec)
- Validates required fields in token payload

### 2. Authentication Middleware (`middleware/auth_middleware.py`)
- Extracts JWT token from Authorization header
- Verifies token using JWT handler
- Attaches authenticated user context to request
- Enforces user isolation at the route level

### 3. Main Application (`main.py`)
- Sets up FastAPI application with authentication
- Includes protected routes
- Validates required environment variables on startup

### 4. Protected Routes (`routes/todos.py`)
- Implements user-isolated CRUD operations
- Each endpoint validates user authentication
- Enforces that users can only access their own data

### 5. Auth Routes (`routes/auth.py`)
- Provides compatibility endpoints for login, registration, and session management
- Works with JWT tokens from Better Auth

## Security Features

- **Stateless Authentication**: No server-side session storage
- **JWT Verification**: Cryptographic verification of tokens
- **User Isolation**: Users can only access their own resources
- **Token Expiration**: Automatic token expiry enforcement
- **Environment Validation**: Ensures required secrets are set

## Environment Variables

- `BETTER_AUTH_SECRET`: Shared secret key for JWT signing/verification (required)
- `DATABASE_URL`: Database connection string (required)

## API Endpoints

### Authentication Endpoints
- `POST /auth/login` - User login (compatibility endpoint)
- `POST /auth/register` - User registration (compatibility endpoint)
- `POST /auth/logout` - User logout (compatibility endpoint)
- `GET /auth/session` - Get current session (requires JWT)

### Protected Endpoints (require JWT token)
- `GET /profile` - Get authenticated user profile
- `GET /todos/` - Get user's todos
- `POST /todos/` - Create new todo
- `GET /todos/{id}` - Get specific todo
- `PUT /todos/{id}` - Update specific todo
- `DELETE /todos/{id}` - Delete specific todo
- `DELETE /todos/` - Delete all user's todos

### Public Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check

## Usage

1. Set the `BETTER_AUTH_SECRET` and `DATABASE_URL` environment variables
2. Start the backend server:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Send requests with Authorization header:
   ```
   Authorization: Bearer <JWT_TOKEN>
   ```

## Compliance with Specification

This implementation satisfies all requirements from the authentication specification:

✅ All protected API routes require a valid JWT  
✅ JWT tokens are issued by Better Auth and verified by FastAPI  
✅ User identity is derived only from verified JWT payload  
✅ URL user_id matches authenticated user_id  
✅ Requests without valid token return HTTP 401  
✅ Requests with mismatched user_id return HTTP 403  
✅ JWT verification implemented as FastAPI middleware  
✅ All database queries filtered by authenticated user ID  
✅ No endpoint bypasses authentication  
✅ Token expiry enforced (≤ 7 days)  
✅ Backend is stateless (no session storage)  
✅ Shared secret provided via environment variable  
✅ Both frontend and backend fail startup if secret is missing