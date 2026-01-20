# Clarification: Fix Better Auth, Neon DB, and Next.js 16 Implementation

## Areas Requiring Clarification

### 1. Project Structure
**Question:** Is the current directory structure exactly `frontend/my-app` inside the main project directory, or could there be variations?
**Clarification:** The prompt indicates there's a `frontend` folder AND a nested `frontend/my-app` folder that needs to be flattened.

### 2. Next.js Version
**Question:** Should we use Next.js 14.2.x, 15.x, or latest stable? The prompt mentions multiple options.
**Clarification:** Will determine the latest stable version that's compatible with Better Auth and use that.

### 3. Database Schema Details
**Question:** What exactly are the "standard Better Auth User, Session, Account, Verification schemas" that need to be pasted?
**Clarification:** Need to reference Better Auth documentation for the exact schema definitions required.

### 4. Backend Integration
**Question:** How does the frontend authentication connect with the backend FastAPI? Are there shared secrets or tokens?
**Clarification:** The `BETTER_AUTH_SECRET` should match between frontend and backend for proper integration.

### 5. Error Handling Specifics
**Question:** What constitutes a "clean error message" versus causing a crash?
**Clarification:** Error handling should catch network errors and return user-friendly messages rather than letting exceptions bubble up.

### 6. Prisma Adapter Configuration
**Question:** Are there specific configurations needed for Neon DB with the Prisma adapter beyond the standard setup?
**Clarification:** Need to ensure the PostgreSQL provider is explicitly set for Neon compatibility.

## Assumptions

### 1. File Locations
- The `lib/auth.ts` file exists or needs to be created
- The `prisma/schema.prisma` file exists or needs to be created
- The `lib/api.ts` file exists or needs to be updated

### 2. Dependencies
- Node.js and npm are available in the environment
- Prisma CLI is available or needs to be installed
- Git is available for version control (if needed)

### 3. Environment
- Local development environment with access to Neon DB
- Backend FastAPI server running at the specified URL
- Ability to create and modify environment files

## Open Questions

### 1. Authentication Flow
Does the application require any specific authentication flows beyond standard username/password?

### 2. User Roles/Permissions
Are there specific role-based access controls that need to be preserved during the fix?

### 3. Existing Data
Is there existing user data in the database that needs to be preserved during schema updates?

### 4. Testing Requirements
Are there existing tests that need to pass after the changes, or should new tests be created?

## Decisions Made

### 1. Execution Order
Following the exact order specified in the prompt:
1. Clean folder structure
2. Install dependencies
3. Update environment variables
4. Run Prisma generate and push
5. Start server and verify endpoints

### 2. Error Handling Approach
Using try/catch blocks around API calls with appropriate error messaging to prevent crashes.

### 3. Runtime Selection
Using standard Node.js runtime instead of edge-specific runtime to avoid adapter initialization errors.