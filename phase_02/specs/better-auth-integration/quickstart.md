# Quickstart Guide: Better Auth Integration

## Prerequisites

- Node.js 18+ installed
- Next.js 14.0.4+ installed
- A running backend server with JWT validation
- Git for version control

## Installation

1. **Install Better Auth dependencies:**
   ```bash
   cd frontend
   npm install better-auth better-auth/react
   ```

2. **Verify existing dependencies:**
   ```bash
   # Check that these are already installed
   npm list next react react-dom jose
   ```

## Configuration

1. **Set up Better Auth client:**
   Create `frontend/lib/auth.ts` with the following configuration:
   ```typescript
   import { createAuthClient } from "better-auth/react";
   import { bearerClient } from "better-auth/client/plugins";

   export const auth = createAuthClient({
     baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:8080',
     plugins: [bearerClient()]
   });
   ```

2. **Configure environment variables:**
   Create or update `.env.local` in the frontend directory:
   ```
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8080
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

## Basic Implementation

1. **Create Auth Context:**
   Set up authentication state management in `frontend/lib/auth-context.tsx`:
   ```jsx
   import { createContext, useContext, useState, useEffect } from 'react';
   import { auth } from './auth';

   const AuthContext = createContext();

   export function AuthProvider({ children }) {
     const [user, setUser] = useState(null);
     const [loading, setLoading] = useState(true);

     useEffect(() => {
       const checkAuth = async () => {
         try {
           const session = await auth.getSession();
           if (session?.user) {
             setUser(session.user);
           }
         } finally {
           setLoading(false);
         }
       };
       
       checkAuth();
     }, []);

     // ... signIn, signOut, and other auth methods
   }
   ```

2. **Update API utilities:**
   Modify `frontend/lib/api.ts` to use Better Auth tokens:
   ```typescript
   export async function authenticatedRequest(url, options = {}) {
     const session = await auth.getSession();
     
     if (!session) {
       throw new Error('Not authenticated');
     }

     const fetchOptions = {
       ...options,
       headers: {
         ...options.headers,
         'Authorization': `Bearer ${session.token}`,
         'Content-Type': 'application/json',
       },
       credentials: 'include',
     };

     return fetch(url, fetchOptions);
   }
   ```

## Running the Application

1. **Start the backend:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Start the frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the application:**
   Visit `http://localhost:3000` in your browser

## Testing Authentication

1. **Verify auth state:**
   - Check that the auth context properly initializes
   - Verify that session tokens are being stored and retrieved

2. **Test protected routes:**
   - Navigate to protected pages
   - Verify that unauthorized access is properly blocked

3. **Test token refresh:**
   - Monitor token expiration and refresh behavior
   - Verify that sessions persist across browser restarts

## Troubleshooting

- **Token not refreshing**: Check that the backend JWT validation accepts Better Auth tokens
- **CORS errors**: Ensure backend allows requests from frontend origin
- **Session not persisting**: Verify that cookies are enabled and properly configured