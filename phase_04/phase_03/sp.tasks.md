# Tasks: Fix Better Auth, Neon DB, and Next.js 16 Implementation

## Task List

### 1. Project Hygiene (Critical)
- [ ] Flatten project structure: Move all source code from `frontend/my-app` to `frontend/`
- [ ] Delete the `my-app` folder entirely after moving files
- [ ] Clean configuration: Delete any `next.config.js` or `eslint.config.js` if TypeScript versions (`.ts`) exist
- [ ] Update `package.json` to include required dependencies:
  - `"next": "14.2.x"` or `"15.x"` (or "latest stable")
  - `"better-auth": "^1.1.0"`
  - `"@prisma/client": "latest"`
  - `"pg": "latest"`

### 2. Environment & Neon DB Setup
- [ ] Create/Update `.env.local` in the `frontend` root with required keys:
  - `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000`
  - `BETTER_AUTH_URL=http://localhost:3000`
  - `BETTER_AUTH_SECRET=your_secure_random_string_here`
  - `DATABASE_URL="postgres://user:password@ep-host.aws.neon.tech/neondb?sslmode=require"`
- [ ] Verify environment variables are properly loaded

### 3. Auth Configuration (Next.js 16 Standard)
- [ ] Update `lib/auth.ts` with Better Auth configuration using Prisma adapter
- [ ] Configure database adapter with standard Node.js runtime (not edge-specific)
- [ ] Set up email and password authentication
- [ ] Configure trusted origins for CORS settings

### 4. Database Schema (Prisma + Neon)
- [ ] Update `prisma/schema.prisma` with proper generator and datasource
- [ ] Add Better Auth User, Session, Account, and Verification schemas
- [ ] Ensure "User" table includes an "id" field matching backend expectations
- [ ] Run `npx prisma generate` after schema update
- [ ] Run `npx prisma db push` after schema update

### 5. API Client Fix (ECONNREFUSED Fix)
- [ ] Update `lib/api.ts` to use `authClient.getSession()` to get tokens
- [ ] Wrap fetch calls in try/catch blocks
- [ ] Implement error handling to return clean error messages instead of crashing
- [ ] Add check for `NEXT_PUBLIC_API_URL` existence

### 6. Execution and Verification
- [ ] Install dependencies (`npm install pg @prisma/client`)
- [ ] Start the server (`npm run dev`)
- [ ] Verify `/api/auth/session` returns valid JSON (or null) and NOT a 500 error
- [ ] Test authentication flow end-to-end
- [ ] Verify error handling works when backend is offline

## Test Cases

### TC-001: Project Structure Validation
**Given:** Nested project structure exists (`frontend/my-app`)
**When:** Structure flattening is performed
**Then:** All files are moved to `frontend/` and `my-app` folder is deleted

### TC-002: Dependency Installation
**Given:** Updated package.json with required dependencies
**When:** `npm install` is executed
**Then:** All dependencies are installed without conflicts

### TC-003: Environment Configuration
**Given:** Environment variables are set in `.env.local`
**When:** Application starts
**Then:** Variables are properly loaded and accessible

### TC-004: Auth Configuration
**Given:** Better Auth is configured with Prisma adapter
**When:** Auth endpoints are accessed
**Then:** Authentication works without adapter initialization errors

### TC-005: Database Connection
**Given:** Prisma schema is configured for Neon DB
**When:** `npx prisma generate` and `npx prisma db push` are executed
**Then:** Schema is generated and pushed to database successfully

### TC-006: API Error Handling
**Given:** Backend is offline or unreachable
**When:** API calls are made from frontend
**Then:** Frontend handles errors gracefully without crashing

### TC-007: Session Endpoint
**Given:** Application is running with proper configuration
**When:** `/api/auth/session` endpoint is accessed
**Then:** Returns valid JSON (or null) and NOT a 500 error