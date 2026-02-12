---
id: 0001
title: Amend constitution for JWT auth
stage: constitution
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: AsfaQasim <asfaqasim144@gmail.com>
command: sp.constitution
labels: [constitution,auth,jwt,security]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - F:\hackthone_todo_vibecode\phase_02\.specify\memory\constitution.md
 - F:\hackthone_todo_vibecode\phase_02\CLAUDE.md
tests:
 - (not run)
---

## Prompt

sp.constitution /sp.constitution

Project: Hackathon Phase II – Multi-User Todo Web Application
Spec: Authentication & User Isolation (Spec 1)

Purpose:
Establish a secure, stateless authentication foundation that enables user-specific
data isolation across frontend and backend services using JWT-based verification.

Core Principles:
- Security-first design (no unauthenticated access)
- Stateless authentication via JWT
- Strict user isolation at API level
- Backend trust through cryptographic verification (not frontend calls)
- Spec-driven, reproducible behavior

Key Standards:
- All protected API routes MUST require a valid JWT
- JWT tokens MUST be issued by Better Auth
- JWT tokens MUST be verified by FastAPI using a shared secret
- User identity MUST be derived ONLY from verified JWT payload
- URL user_id MUST match authenticated user_id
- Requests without valid token MUST return HTTP 401
- Requests with mismatched user_id MUST return HTTP 403

Authentication Rules:
- Better Auth runs ONLY on Next.js frontend
- FastAPI backend NEVER trusts frontend session directly
- JWT token MUST be sent via:
  Authorization: Bearer <token>
- Token verification MUST include:
  - Signature validation
  - Expiry validation
  - Payload decoding

Shared Secret Constraint:
- JWT signing and verification MUST use the same secret key
- Secret MUST be provided via environment variable:
  BETTER_AUTH_SECRET
- Secret MUST NOT be hardcoded in source files
- Both frontend and backend MUST fail startup if secret is missing

Backend Authorization Logic:
- JWT verification MUST be implemented as FastAPI middleware or dependency
- Middleware MUST:
  - Extract Authorization header
  - Validate JWT
  - Attach authenticated user context to request
- All database queries MUST be filtered by authenticated user ID
- Task ownership MUST be enforced at every operation

Security Constraints:
- No endpoint may bypass authentication
- No user may access or mutate another user’s data
- Token expiry MUST be enforced (recommended: ≤ 7 days)
- Backend MUST be stateless (no session storage)

Technology Constraints:
- Frontend: Next.js 16+ (App Router)
- Authentication: Better Auth (JWT plugin enabled)
- Backend: Python FastAPI
- JWT Library: Industry-standard JWT verification
- Spec-Driven Tooling: Claude Code + Spec-Kit Plus

Success Criteria:
- Unauthenticated requests return 401 Unauthorized
- Authenticated users can only access their own resources
- JWT verification succeeds independently on frontend and backend
- No backend endpoint relies on frontend session validation
- Security review passes for user isolation and stateless auth

## Response snapshot

- Updated `.specify/memory/constitution.md` by filling the template with concrete principles and constraints for JWT-based auth and strict user isolation.
- Added a Sync Impact Report and initialized versioning metadata (0.1.0) with today as ratified/amended date.
- Synced CLAUDE.md to match the constitution’s rule: URL `user_id` must match JWT `user_id`; mismatch returns 403.
- Checked Spec-Kit templates; no conflicts found. Located command templates under `.claude/commands/` rather than `.specify/templates/commands/`.

## Outcome

- ✅ Impact: Constitution now defines the security model (JWT auth + isolation) as a non-negotiable project governance rule.
- 🧪 Tests: Not run (documentation-only changes).
- 📁 Files: Updated constitution and CLAUDE.md; created constitution PHR file.
- 🔁 Next prompts: If needed, revise constitution version/date once original ratification date is known.
- 🧠 Reflection: Keep constitution enforceable (MUST/403/401 rules) and align helper docs to avoid contradictions.

## Evaluation notes (flywheel)

- Failure modes observed: Bash script `.specify/scripts/bash/create-phr.sh` not present on this repo/OS path.
- Graders run and results (PASS/FAIL): not run
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Add a Windows-compatible PHR creation script if desired.
