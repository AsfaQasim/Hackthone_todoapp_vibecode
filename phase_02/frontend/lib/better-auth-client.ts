// lib/better-auth-client.ts

import { auth } from './auth-client';

// Better Auth client configuration
// This integrates with the custom auth client that works with our Python backend
class BetterAuthClient {
  // Get the session token from Better Auth
  async getSessionToken(): Promise<string | null> {
    try {
      // Get token from localStorage
      const token = localStorage.getItem('access_token');
      return token;
    } catch (error) {
      console.error('Error getting session token:', error);
      return null;
    }
  }

  // Alternative: If using Authorization header
  async getAuthToken(): Promise<string | null> {
    // This returns the session token from Better Auth
    return this.getSessionToken();
  }

  // Login function (integrates with our custom auth)
  async login(email: string, password: string): Promise<{ success: boolean; error?: string }> {
    try {
      await auth.signIn(email, password);
      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: error instanceof Error ? error.message : 'Login failed' };
    }
  }

  // Signup function (integrates with our custom auth)
  async signup(email: string, password: string, name: string): Promise<{ success: boolean; error?: string }> {
    try {
      await auth.signUp(email, password, name);
      return { success: true };
    } catch (error) {
      console.error('Signup error:', error);
      return { success: false, error: error instanceof Error ? error.message : 'Signup failed' };
    }
  }

  // Logout function (integrates with our custom auth)
  async logout(): Promise<{ success: boolean; error?: string }> {
    try {
      await auth.signOut();
      return { success: true };
    } catch (error) {
      console.error('Logout error:', error);
      return { success: false, error: error instanceof Error ? error.message : 'Logout failed' };
    }
  }

  // Check if session needs refresh
  async needsRefresh(): Promise<boolean> {
    try {
      const session = await auth.getSession();
      if (!session) {
        return true; // Needs refresh if no session
      }

      // Check if session is close to expiration (within 10 minutes)
      const tenMinutesInMillis = 10 * 60 * 1000;
      const sessionExpiresAt = new Date(session.data.expiresAt).getTime();
      const currentTime = Date.now();
      const timeUntilExpiration = sessionExpiresAt - currentTime;

      return timeUntilExpiration < tenMinutesInMillis;
    } catch (error) {
      console.error('Error checking if refresh is needed:', error);
      return true; // Default to needing refresh on error
    }
  }

  // Refresh session
  async refreshSession(): Promise<{ success: boolean; error?: string }> {
    try {
      // For our custom auth, refreshing means revalidating the session
      // which happens automatically when calling getSession()
      const session = await auth.getSession();
      if (session) {
        return { success: true };
      } else {
        return { success: false, error: 'Unable to refresh session' };
      }
    } catch (error) {
      console.error('Error refreshing session:', error);
      return { success: false, error: error instanceof Error ? error.message : 'Session refresh failed' };
    }
  }
}

export const betterAuthClient = new BetterAuthClient();