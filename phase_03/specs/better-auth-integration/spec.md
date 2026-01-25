# Specification: `better-auth` Integration

## 1. Overview

This document specifies the requirements for replacing the current broken, insecure, and custom-built authentication system with a standardized, secure, and efficient implementation using the `better-auth` library. The existing system suffers from critical security vulnerabilities (XSS via `localStorage`), inefficient polling, and incomplete features. This effort will completely remove the faulty implementation and replace it with `better-auth`.

## 2. Functional Requirements

- **FR1: Secure User Registration & Login:** Users must be able to create an account and log in via a secure endpoint. All authentication logic will be handled by `better-auth`.
- **FR2: Protected Routes:** Application routes designated as "protected" must only be accessible to authenticated users. Unauthenticated users attempting to access these routes must be redirected to the login page.
- **FR3: Session Management:** Authenticated users must have a persistent session that survives page reloads. The session state will be managed by `better-auth`'s `SessionProvider`.
- **FR4: Secure Logout:** Users must be able to log out, which will securely invalidate their session and redirect them to a public page (e.g., the homepage or login page).

## 3. Non-Functional Requirements

- **NFR1: Security:**
    - JWTs or session tokens **MUST NOT** be stored in `localStorage`. `better-auth`'s default secure, HTTP-only cookie mechanism will be used.
    - The `better-auth` API endpoints **MUST** be used for all authentication and session-related operations.
    - All custom, client-side authentication logic **MUST** be removed.
- **NFR2: Performance:**
    - The existing `setInterval` polling mechanism for checking session status **MUST** be removed.
    - Session state will be managed efficiently by the `better-auth/react` `useSession` hook, which avoids unnecessary network requests.
- **NFR3: Maintainability:** The new implementation must follow `better-auth`'s documented best practices to ensure the code is clean, maintainable, and easy to upgrade in the future.

## 4. User Stories

- **US1: Login:** As a guest, I want to log in with my credentials so that I can access my account and protected content, being redirected to the dashboard page (`/dashboard`) after successful login.
- **US2: Persist Session:** As a logged-in user, I want my session to be remembered when I reload the page so that I don't have to log in again.
- **US3: Access Content:** As a logged-in user, I want to access dashboard and task pages so that I can manage my information.
- **US4: Logout:** As a logged-in user, I want to securely log out of my account so that my session is terminated.

## Clarifications

### Session 2026-01-13
- Q: After a successful login, where should the user be redirected? → A: To a single, static page (e.g., `/dashboard`).
- Q: How should the application handle a failed login attempt? → A: Specify whether the username or password was incorrect.

## 5. Out of Scope

- Password reset functionality.
- "Remember me" functionality beyond the standard session persistence.
- Social logins (e.g., Google, GitHub).
- Two-factor authentication.

## 6. Edge Cases & Failure Handling

- **Login Failure:** On a failed login attempt, the application will indicate whether the username or password provided was incorrect.
