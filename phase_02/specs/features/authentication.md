# Feature: User Authentication

## User Stories
- As a user, I can sign up with email and password
- As a user, I can sign in with email and password
- As a signed-in user, my identity is verified on backend requests
- As a signed-in user, I can only access my own data

## Acceptance Criteria

### Sign Up
- Email must be unique
- Password must meet minimum security requirements
- User account is created in Better Auth

### Sign In
- Valid credentials allow access to application
- JWT token is issued upon successful authentication
- Token is used for subsequent API requests

### Authentication Verification
- All API endpoints require valid JWT token
- Requests without token receive 401 Unauthorized
- User ID in token matches user ID in request path
- Each user only sees/modifies their own tasks