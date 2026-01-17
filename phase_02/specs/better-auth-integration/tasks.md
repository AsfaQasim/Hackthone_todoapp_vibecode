# Tasks: Better Auth Integration

This document outlines the tasks required to implement the `better-auth` integration as specified in the [spec.md](spec.md) and [plan.md](plan.md) files.

## Feature: Better Auth Integration

The goal is to replace the current broken, insecure, and custom-built authentication system with a standardized, secure, and efficient implementation using the `better-auth` library.

## Dependencies

- User Story 1 (US1: Login) must be completed before US3 (Access Content)
- User Story 2 (US2: Persist Session) must be completed before US3 (Access Content)
- User Story 4 (US4: Logout) can be implemented in parallel with other stories

## Parallel Execution Opportunities

- US1 (Login) and US4 (Logout) can be developed in parallel after foundational setup
- US2 (Persist Session) and US3 (Access Content) can be developed in parallel after US1 is complete

---

## Phase 1: Setup

### Goal
Initialize the project with necessary dependencies and configurations for better-auth integration.

### Tasks

- [ ] T001 Create backend directory structure with subdirectories: utils, middleware, models, routes
- [ ] T002 Install required backend dependencies in backend/requirements.txt: fastapi, pyjwt, python-multipart, python-dotenv, sqlmodel, psycopg2-binary
- [ ] T003 Set up BETTER_AUTH_SECRET environment variable validation in backend application startup
- [ ] T004 [P] Create frontend lib directory if it doesn't exist
- [ ] T005 [P] Install better-auth dependencies in frontend: better-auth, better-auth/react

---

## Phase 2: Foundational

### Goal
Implement core authentication infrastructure that will be used by all user stories.

### Tasks

- [ ] T006 Implement JWT handler utility in backend/utils/jwt_handler.py with create and verify functions
- [ ] T007 Create authentication middleware in backend/middleware/auth_middleware.py with JWTBearer class
- [ ] T008 [P] Create main FastAPI application in backend/main.py with authentication dependencies
- [ ] T009 [P] Create todos route in backend/routes/todos.py with authentication protection
- [ ] T010 [P] Create frontend auth client in frontend/lib/auth.ts with better-auth configuration
- [ ] T011 [P] Update frontend environment variables in .env.local with BETTER_AUTH_SECRET and API URLs
- [ ] T012 [P] Create API utility functions in frontend/lib/api.ts for authenticated requests

---

## Phase 3: [US1] Login

### Goal
As a guest, I want to log in with my credentials so that I can access my account and protected content, being redirected to the dashboard page (`/dashboard`) after successful login.

### Independent Test Criteria
- User can submit login form with email and password
- Successful login redirects to /dashboard
- Failed login shows appropriate error message
- JWT token is properly stored and used for subsequent requests

### Tasks

- [ ] T013 [US1] Create login API endpoint in backend/routes/auth.py for handling login requests
- [ ] T014 [US1] Update frontend AuthComponent.tsx to use better-auth signIn function
- [ ] T015 [US1] Implement login form validation and error handling in frontend/components/AuthComponent.tsx
- [ ] T016 [US1] Configure redirect to /dashboard after successful login in frontend
- [ ] T017 [US1] Add login failure handling with specific error messages in frontend
- [ ] T018 [US1] Test login flow with valid credentials and verify JWT token generation
- [ ] T019 [US1] Test login flow with invalid credentials and verify appropriate error response

---

## Phase 4: [US2] Persist Session

### Goal
As a logged-in user, I want my session to be remembered when I reload the page so that I don't have to log in again.

### Independent Test Criteria
- Session persists after page refresh
- Session data is correctly retrieved from storage
- User remains authenticated across browser restarts
- Session expires appropriately according to configured timeout

### Tasks

- [ ] T020 [US2] Implement SessionProvider in frontend/app/layout.tsx to wrap the application
- [ ] T021 [US2] Create session context management in frontend/lib/auth-context.tsx
- [ ] T022 [US2] Implement session persistence using better-auth's client-side storage
- [ ] T023 [US2] Add session validation on page load to check authentication status
- [ ] T024 [US2] Implement automatic token refresh before expiration
- [ ] T025 [US2] Test session persistence across page refreshes
- [ ] T026 [US2] Test session persistence across browser restarts
- [ ] T027 [US2] Test session expiration and cleanup

---

## Phase 5: [US3] Access Content

### Goal
As a logged-in user, I want to access dashboard and task pages so that I can manage my information.

### Independent Test Criteria
- Authenticated users can access protected routes
- Unauthenticated users are redirected to login when accessing protected routes
- Users can only access their own data (user isolation enforced)
- API requests include valid JWT tokens in headers

### Tasks

- [ ] T028 [US3] Create protected dashboard route in frontend/app/dashboard/page.tsx
- [ ] T029 [US3] Implement route protection middleware in frontend/middleware.ts using better-auth
- [ ] T030 [US3] Update todos API endpoints in backend/routes/todos.py to enforce user isolation
- [ ] T031 [US3] Create task management components in frontend that use authenticated API calls
- [ ] T032 [US3] Implement user ID validation in backend to ensure data isolation
- [ ] T033 [US3] Test access to protected routes when authenticated
- [ ] T034 [US3] Test redirection to login when accessing protected routes without authentication
- [ ] T035 [US3] Test that users can only access their own data

---

## Phase 6: [US4] Logout

### Goal
As a logged-in user, I want to securely log out of my account so that my session is terminated.

### Independent Test Criteria
- Logout function clears all session data
- User is redirected to public page after logout
- Subsequent requests without re-authentication are denied
- Session tokens are properly invalidated

### Tasks

- [ ] T036 [US4] Create logout API endpoint in backend/routes/auth.py for handling logout requests
- [ ] T037 [US4] Update LogoutButton.tsx component to use better-auth signOut function
- [ ] T038 [US4] Implement secure session termination in backend
- [ ] T039 [US4] Configure redirect after logout to homepage or login page
- [ ] T040 [US4] Clear all client-side session storage on logout
- [ ] T041 [US4] Test logout functionality and verify session termination
- [ ] T042 [US4] Test that authenticated requests fail after logout

---

## Phase 7: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with security enhancements, error handling, and documentation.

### Tasks

- [ ] T043 Add comprehensive error handling for all authentication flows
- [ ] T044 Implement proper security headers for all API responses
- [ ] T045 Add logging for authentication events (login, logout, failed attempts)
- [ ] T046 Create comprehensive README documentation for authentication system
- [ ] T047 Add input validation and sanitization to prevent injection attacks
- [ ] T048 Perform security audit of authentication implementation
- [ ] T049 Test edge cases and failure scenarios
- [ ] T050 Update API documentation with authentication requirements

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)
Focus on completing User Story 1 (Login) and User Story 3 (Access Content) to establish the core authentication flow. This includes:
- Basic login functionality with credential validation
- JWT token generation and verification
- Protected routes that require authentication
- Basic user isolation for data access

### Incremental Delivery
1. Complete Phase 1-3: Setup, Foundation, and Login (US1)
2. Add Phase 4: Session Persistence (US2) 
3. Add Phase 5: Content Access (US3)
4. Complete with Phase 6-7: Logout (US4) and Polish

This approach allows for early validation of the authentication system while progressively adding features.