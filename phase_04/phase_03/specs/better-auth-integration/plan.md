# Architectural Plan: `better-auth` Integration

## 1. Overview

This plan outlines the technical approach to replacing the legacy, insecure authentication system with `better-auth`. The strategy is to completely remove the old implementation before integrating the new one to ensure a clean, conflict-free migration.

## 2. Phases

### Phase 1: Removal of Legacy Authentication System

The first and most critical step is to remove all components of the old, custom-built authentication system. This prevents any possibility of legacy code conflicting with the `better-auth` implementation.

**Files to be Deleted:**
- `frontend/lib/auth.ts`: Contains the insecure custom auth client and `useSession` hook.
- `frontend/lib/auth-context.tsx`: The core of the broken system, with inefficient polling.
- `frontend/lib/better-auth-client.ts`: The misleading and non-functional wrapper.
- `frontend/components/AuthProvider.tsx`: The provider component for the old context.

### Phase 2: Backend Configuration for `better-auth`

We will create the backend API endpoint that `better-auth` requires to handle all authentication requests (login, logout, session management).

- **Create `better-auth` API Route:** A new file will be created at `frontend/pages/api/auth/[...betterauth].ts`. This file will handle all dynamic authentication routes.
- **Configure Providers:** The API route will be configured with the "Credentials" provider to allow users to log in with an email and password. This will involve validating user credentials against the database.

### Phase 3: Frontend Integration

With the backend in place, we will integrate `better-auth` into the Next.js frontend.

- **Implement `SessionProvider`:** The root layout (`frontend/app/layout.tsx`) will be wrapped with the `SessionProvider` from `better-auth/react`. This makes the session context available throughout the application.
- **Replace Middleware:** The existing, non-functional middleware at `frontend/middleware.ts` will be deleted and replaced with a new version that correctly uses `better-auth`'s middleware functionality to protect routes.
- **Refactor UI Components:**
    - `frontend/components/AuthComponent.tsx`: Will be updated to use `better-auth`'s `signIn` function instead of the old, custom hook.
    - `frontend/components/Header.tsx` / `frontend/components/LogoutButton.tsx`: Will be updated to use the `useSession` and `signOut` hooks from `better-auth/react`.
    - Any other component relying on the old `useAuth` hook will be refactored.

## 3. Data Model & Interfaces

No changes are required to the existing user data model in the database. The `better-auth` credentials provider will interface with the existing `users` table to verify credentials. The frontend will interact exclusively with the `better-auth` client-side library (`useSession`, `signIn`, `signOut`).

## 4. Key Decisions & Rationale

- **Decision: Complete Removal of Old Code:** Instead of attempting a partial migration, a complete rip-and-replace approach was chosen.
  - **Rationale:** The old code is fundamentally insecure and inefficient. It is safer and cleaner to remove it entirely than to risk leaving flawed code in the codebase.
- **Decision: Use `better-auth`'s Standard Features:** We will adhere to the standard implementation patterns provided in the `better-auth` documentation.
  - **Rationale:** This ensures security, maintainability, and access to the full feature set of the library, including session management and CSRF protection.

## 5. Risk Analysis

- **Risk:** Incorrectly configuring the `better-auth` API route could lead to authentication failures.
  - **Mitigation:** Follow the official `better-auth` documentation closely and test the login/logout flow thoroughly.
- **Risk:** Protected routes may not be properly secured if the new middleware is misconfigured.
  - **Mitigation:** Test route protection by attempting to access protected pages both as an authenticated and unauthenticated user.
