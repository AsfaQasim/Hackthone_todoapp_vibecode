# Secure Todo Web Application

This is a multi-user todo web application with secure authentication and user isolation implemented according to the specification.

## Architecture

- **Frontend**: Next.js 14+ with App Router
- **Authentication**: Better Auth with JWT tokens
- **Backend**: FastAPI with JWT verification middleware
- **Database**: In-memory storage (for demo purposes)

## Features Implemented

### Authentication System
- User sign up and sign in using Better Auth
- JWT token issuance with user_id, email, and expiration
- Token transport using Authorization header
- Stateless authentication (no sessions stored)

### User Isolation
- Each user can only access their own tasks
- Backend enforces user identity on every request
- Users cannot access, modify, or delete other users' data

### Security Measures
- All API endpoints require authentication
- JWT verification includes signature validation and expiry check
- Environment variables for secrets (not committed to source control)
- Proper error handling for unauthorized access

## Project Structure

```
phase_02/
├── frontend/                 # Next.js frontend
│   ├── app/                  # App Router pages
│   ├── components/           # React components
│   ├── lib/                  # Utility functions
│   └── ...
├── backend/                  # FastAPI backend
│   ├── api/                  # API route definitions
│   ├── models/               # Data models
│   ├── schemas/              # Pydantic schemas
│   ├── utils/                # Utility functions
│   └── main.py               # Main application entrypoint
├── README.md                 # This file
└── ...
```

## Setup Instructions

### Prerequisites
- Node.js 18+
- Python 3.8+

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Create a `.env.local` file with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-change-in-production
   BASE_URL=http://localhost:3000
   ```
4. Start the development server: `npm run dev`

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with:
   ```
   BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-change-in-production
   BACKEND_HOST=0.0.0.0
   BACKEND_PORT=8000
   FRONTEND_URL=http://localhost:3000
   ```
4. Start the server: `python main.py`

### Running the Application
1. Start the backend server first: `cd backend && python main.py`
2. In a new terminal, start the frontend: `cd frontend && npm run dev`
3. Access the application at `http://localhost:3000`

## API Endpoints

### Health Check
- `GET /health` - Check if the API is running

### Todo Operations (require authentication)
- `GET /todos/` - Get all todos for the authenticated user
- `POST /todos/` - Create a new todo for the authenticated user
- `GET /todos/{id}` - Get a specific todo by ID
- `PUT /todos/{id}` - Update a specific todo
- `DELETE /todos/{id}` - Delete a specific todo
- `GET /todos/count` - Get the count of user's todos
- `DELETE /todos/` - Delete all of user's todos

### Authentication Headers
All authenticated endpoints require:
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

## Security Validation

The implementation satisfies all security constraints from the specification:

1. ✅ All task-related API endpoints require authentication
2. ✅ No endpoint bypasses JWT verification
3. ✅ Token expiry is enforced (7-day maximum)
4. ✅ Secrets are loaded from environment variables
5. ✅ Stateless authorization - all decisions derived from JWT alone
6. ✅ Backend functions independently of frontend runtime state
7. ✅ User ID in request path is verified against authenticated user ID
8. ✅ Backend does not trust frontend-provided user ID without verification

## Testing

To manually test the authentication flow and user isolation:

1. Create two different user accounts
2. Log in as the first user and create some todos
3. Log out and log in as the second user
4. Verify that the second user cannot see the first user's todos
5. Verify that each user can only modify their own todos

## Environment Variables

Both frontend and backend require the `BETTER_AUTH_SECRET` environment variable. This should be a strong, random secret in production.

## Compliance with Specification

This implementation fully complies with the Authentication & User Isolation specification:
- Implements secure, stateless authentication
- Ensures only authenticated users can access the API
- Enforces that each user can only access and modify their own tasks
- Operates with frontend and backend independently using JWT verification
- Maintains user isolation on every request