# Specification: Fix Better Auth, Neon DB, and Next.js 16 Implementation

## Overview
Fix a broken authentication implementation in a project using **Next.js 16 (Stable App Router)**, **Better Auth**, **FastAPI**, and **Neon DB (PostgreSQL)**. The current project state has critical configuration errors (nested folders, connection refusals, and database adapter failures).

## Goals
1. Flatten project structure and eliminate version conflicts
2. Establish solid connection to Neon DB
3. Initialize Better Auth with Prisma adapter correctly
4. Ensure database schema has required Better Auth tables
5. Fix API client to prevent crashes when backend is unreachable
6. Ensure proper execution order of setup steps

## Requirements
### Functional Requirements
- Authentication should work properly with Better Auth and Neon DB
- Frontend should not crash when backend is offline
- Database connections should be established properly
- API calls should be wrapped in try/catch blocks

### Technical Requirements
- Next.js 14.2.x or 15.x (or latest stable)
- Better Auth version ^1.1.0
- Prisma Client (latest)
- PostgreSQL driver (pg package)
- Neon DB connection using proper URL format
- Proper environment variable configuration

### Constraints
- Use standard Node.js runtime for database adapter
- Ensure CORS/trusted origin settings are properly configured
- Follow Next.js 16 App Router conventions
- Maintain compatibility with existing backend

## Acceptance Criteria
- [ ] Project structure is flattened (no nested my-app folder)
- [ ] Dependencies are properly installed and configured
- [ ] Environment variables are set correctly
- [ ] Better Auth is configured with Prisma adapter
- [ ] Database schema includes required Better Auth tables
- [ ] API client handles network errors gracefully
- [ ] Frontend does not crash when backend is unreachable
- [ ] Authentication endpoints return valid responses
- [ ] Prisma generates and pushes schema successfully