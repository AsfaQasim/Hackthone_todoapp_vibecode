# Hackathon Phase II – Multi-User Todo Web Application Constitution
<!--
Sync Impact Report
- Version change: 0.0.0 → 0.1.0
- Modified principles: N/A (template placeholders replaced)
- Added sections: Additional Constraints, Development Workflow
- Removed sections: None
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (uses constitution gates; no hardcoded gates)
  - ✅ .specify/templates/spec-template.md (no conflicts)
  - ✅ .specify/templates/tasks-template.md (no conflicts)
  - ⚠ pending: .specify/templates/commands/*.md (not reviewed yet)
  - ⚠ pending: repository runtime docs (README, quickstart) not found in repo root
- Deferred TODOs:
  - TODO(RATIFICATION_DATE): original adoption date unknown; set to today for now
-->

## Core Principles

### Security-first: no unauthenticated access
All protected API routes MUST require a valid JWT. Requests without a valid token MUST return
HTTP 401.

Rationale: the system’s baseline security posture is “deny by default”; all access is explicit.

### Stateless authentication via JWT
JWTs MUST be issued by Better Auth on the Next.js frontend and MUST be verified by the
FastAPI backend using a shared secret.

Token verification MUST include:
- Signature validation
- Expiry validation
- Payload decoding

Rationale: the backend must be able to authenticate requests independently without calling
the frontend.

### Strict user isolation at the API + database layer
User identity MUST be derived ONLY from the verified JWT payload.

All database queries MUST be filtered by the authenticated user ID.
Task ownership MUST be enforced at every operation.

Rationale: user isolation is a security boundary; it must be enforced consistently across all
CRUD operations.

### Backend trust through cryptographic verification
FastAPI backend NEVER trusts the frontend session directly.

Rationale: cryptographic verification (JWT) is the trust primitive; not UI state.

### Spec-driven, reproducible behavior
Authentication and authorization behavior MUST be specified in a testable way:
- Missing/invalid token → 401
- Authenticated user can access only their own resources
- Mismatched `user_id` → 403

Rationale: security behavior must be reproducible across environments and implementations.

### Technology constraints are non-negotiable
- Frontend: Next.js 16+ (App Router)
- Authentication: Better Auth (JWT plugin enabled)
- Backend: Python FastAPI
- JWT Library: industry-standard JWT verification
- Database: Neon Serverless PostgreSQL
- ORM: SQLModel
- Spec-driven tooling: Claude Code + Spec-Kit Plus

## Additional Constraints

### Shared secret constraint
- JWT signing and verification MUST use the same secret key.
- Secret MUST be provided via environment variable: `BETTER_AUTH_SECRET`.
- Secret MUST NOT be hardcoded in source files.
- Both frontend and backend MUST fail startup if the secret is missing.

### Authorization binding to URL path
- URL `user_id` MUST match authenticated `user_id`.
- Requests with mismatched `user_id` MUST return HTTP 403.

## Development Workflow

### Implementation placement
JWT verification MUST be implemented as a FastAPI middleware or dependency that:
- Extracts the `Authorization` header
- Validates the JWT
- Attaches authenticated user context to the request

### Quality gates (security)
- No endpoint may bypass authentication.
- No user may access or mutate another user’s data.
- Backend MUST be stateless (no session storage).
- Token expiry MUST be enforced (recommended: ≤ 7 days).

## Governance

- This constitution supersedes other practices and templates when in conflict.
- Amendments MUST:
  - increment the constitution version (semantic versioning)
  - describe the change in a Sync Impact Report (at top of this file)
  - be reviewed for downstream template implications
- Compliance review expectation:
  - security-affecting changes MUST be reviewed for authn/authz regressions
  - PRs SHOULD reference which principles they touch

**Version**: 0.1.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08
