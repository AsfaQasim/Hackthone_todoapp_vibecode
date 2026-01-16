# Tasks: `better-auth` Integration

This file breaks down the work required to implement the `better-auth` integration, as outlined in the `plan.md`.

---

### Phase 1: Removal of Legacy Authentication System

**Task 1.1: Delete Legacy Auth Files**

- **Description:** Delete all files associated with the old, custom authentication system to prepare for a clean installation of `better-auth`.
- **Files to Delete:**
    - `frontend/lib/auth.ts`
    - `frontend/lib/auth-context.tsx`
    - `frontend/lib/better-auth-client.ts`
    - `frontend/components/AuthProvider.tsx`
- **Acceptance Criteria:**
    - [x] The four specified files are deleted from the file system.
    - [x] The application will fail to compile, which is expected.

---

### Phase 2: Backend Configuration for `better-auth`

**Task 2.1: Create `better-auth` API Route**

- **Description:** Create the dynamic API route that `better-auth` uses to handle authentication requests.
- **File to Create:** `frontend/pages/api/auth/[...betterauth].ts`
- **Acceptance Criteria:**
    - [x] The new file is created at the specified path.
    - [x] The file exports a `better-auth` configuration object.
    - [x] The configuration includes a `CredentialsProvider` for email/password login.
    - [ ] The `authorize` function within the provider is wired up to validate user credentials against the backend API.

---

### Phase 3: Frontend Integration

**Task 3.1: Wrap Application in `SessionProvider`**

- **Description:** Wrap the root of the application with `better-auth`'s `SessionProvider` to make session data available globally.
- **File to Modify:** `frontend/app/layout.tsx`
- **Acceptance Criteria:**
    - [x] The `SessionProvider` component from `better-auth/react` is imported.
    - [x] The `SessionProvider` wraps the main content of the layout.

**Task 3.2: Replace Auth Middleware**

- **Description:** Replace the old, insecure middleware with a new middleware that correctly protects routes using `better-auth`.
- **File to Modify:** `frontend/middleware.ts`
- **Acceptance Criteria:**
    - [x] The old middleware file is deleted.
    - [x] A new `middleware.ts` is created that exports the default middleware from `better-auth/middleware`.
    - [x] A `config` object is included to specify the routes the middleware should apply to (e.g., `/dashboard/:path*`, `/tasks/:path*`).

**Task 3.3: Refactor `AuthComponent` for Login**

- **Description:** Update the main authentication form to use `better-auth`'s `signIn` method.
- **File to Modify:** `frontend/components/AuthComponent.tsx`
- **Acceptance Criteria:**
    - [x] The component no longer uses the old `useAuth` hook.
    - [x] The `signIn` function from `better-auth/react` is used to handle form submission.
    - [x] The user is redirected to a protected page on successful login.

**Task 3.4: Refactor Header and Logout Button**

- **Description:** Update the UI to display user session status and handle logout correctly.
- **Files to Modify:** `frontend/components/Header.tsx`, `frontend/components/LogoutButton.tsx` (or similar)
- **Acceptance Criteria:**
    - [x] The `useSession` hook from `better-auth/react` is used to conditionally render login/logout buttons.
    - [x] The `signOut` function from `better-auth/react` is called when the logout button is clicked.

---
