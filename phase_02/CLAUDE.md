# Claude Code Rules (phase_02)

This repository is a **Next.js (App Router) + FastAPI + Neon Postgres** todo app built using **Spec-Driven Development (Spec-Kit Plus)**.

## Surface + success criteria
- **Surface:** project-level engineering assistant (architecture, code changes, debugging, review).
- **Success:** smallest viable diffs; no behavior regressions; clear acceptance checks; precise code references; secure auth boundaries.

## Project overview

### Tech stack
- **Frontend:** Next.js 16+ (App Router)
- **Backend:** Python FastAPI
- **ORM:** SQLModel
- **Database:** Neon Serverless PostgreSQL
- **Spec-driven:** Claude Code + Spec-Kit Plus
- **Authentication:** Better Auth (frontend) + JWT verification (backend)

### REST API (high-level)
Base pattern uses a `user_id` path segment, but **authorization is driven by the JWT** (see below).

- `GET    /api/{user_id}/tasks` — list tasks
- `POST   /api/{user_id}/tasks` — create task
- `GET    /api/{user_id}/tasks/{id}` — get task details
- `PUT    /api/{user_id}/tasks/{id}` — update task
- `DELETE /api/{user_id}/tasks/{id}` — delete task
- `PATCH  /api/{user_id}/tasks/{id}/complete` — toggle completion

### Auth model (Better Auth → JWT → FastAPI)
- Frontend uses Better Auth to create a session and issue a JWT.
- Frontend sends `Authorization: Bearer <token>` on every backend request.
- Backend verifies JWT signature using **the shared secret** (`BETTER_AUTH_SECRET`).
- Backend derives the authenticated user from JWT claims and uses that identity for all reads/writes.

**Source of truth rule:** URL `user_id` **MUST match** authenticated `user_id` from the JWT.
- Backend derives user identity from the JWT.
- If path `user_id` does not match JWT `user_id`, return `403 Forbidden`.
- Every query must be filtered by the authenticated user from the token.

**Expected behavior change after auth is enabled:**
- All endpoints require a valid JWT.
- Missing/invalid token → `401 Unauthorized`.

## Repository workflow rules (must follow)

### Constraints / invariants / non-goals
- Do not invent API contracts; verify in code before stating specifics.
- No secret material committed; use `.env` / environment variables.
- Avoid unrelated refactors; keep diffs minimal and testable.
- Validate at boundaries (HTTP input, external APIs); avoid redundant internal checks.

### Tooling and execution
- Prefer repo tools (CLI + MCP tools) for discovery/verification.
- Don’t propose changes to code you haven’t read.
- When referencing code, include `file_path:line_number`.

## Prompt History Records (PHRs) — mandatory
After completing work for **every user message**, create a PHR under `history/prompts/`.

### Stage routing
- `constitution` → `history/prompts/constitution/`
- Feature stages (`spec|plan|tasks|red|green|refactor|explainer|misc`) → `history/prompts/<feature-name>/`
- `general` → `history/prompts/general/`

### Creation checklist
- Read the PHR template from:
  - `.specify/templates/phr-template.prompt.md` OR
  - `templates/phr-template.prompt.md`
- Allocate an incrementing ID (avoid collisions).
- Fill all placeholders; no `{{...}}` left.
- Include full user prompt verbatim (multiline).
- Report: ID, absolute path, stage, title.

## ADR suggestions (never auto-create)
When a decision is architecturally significant (long-term impact + alternatives + cross-cutting scope), suggest:

> 📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`

Wait for explicit consent before creating ADRs.
