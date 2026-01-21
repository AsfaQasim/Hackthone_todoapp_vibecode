"use client";

import { createAuthClient } from "better-auth/react";

// Client-side Better Auth configuration
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
  // Enable credentials to handle cookies properly
  credentials: 'include',
});

console.log("Auth client initialized:", !!authClient, "Provider exists:", !!authClient?.Provider);

// Export individual methods
export const useSession = authClient.useSession;
export const signIn = authClient.signIn;
export const signUp = authClient.signUp;
export const signOut = authClient.signOut;

// Export the authClient instance for use in API calls
export { authClient };