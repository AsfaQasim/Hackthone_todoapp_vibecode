'use client'

import React from 'react';

// Mock session object for compatibility
const mockSession = {
  data: null,
  isLoading: false,
  update: () => Promise.resolve(),
  mutate: () => Promise.resolve(),
};

// Function to get session (check for our auth token)
export function useSession() {
  if (typeof window !== 'undefined') {
    const cookies = document.cookie.split('; ');
    let tokenExists = false;
    for (let i = 0; i < cookies.length; i++) {
      if (cookies[i].startsWith('auth_token=')) {
        tokenExists = true;
        break;
      }
    }

    if (tokenExists) {
      // In a real app, we would decode the JWT to get user info
      // For now, return a basic user object
      return {
        ...mockSession,
        data: {
          user: { id: '1', email: 'user@example.com' }, // Placeholder
          expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours from now
        }
      };
    }
  }

  return mockSession;
}

// Sign in function
export async function signIn(credentials: { email: string; password: string }, options?: { callbackURL?: string }) {
  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    const data = await response.json();

    if (response.ok) {
      // Store the JWT token in a cookie
      const expirationDate = new Date();
      expirationDate.setDate(expirationDate.getDate() + 1); // 1 day from now

      // Create cookie string without using template literals or regex-sensitive characters
      const cookieParts = [
        'auth_token=' + data.token,
        'path=/',
        'expires=' + expirationDate.toUTCString(),
        'SameSite=Lax'
      ];
      document.cookie = cookieParts.join('; ');

      // Redirect if callbackURL is provided
      if (options?.callbackURL) {
        window.location.href = options.callbackURL;
      }

      return { error: null, data };
    } else {
      return { error: { message: data.error || 'Login failed' }, data: null };
    }
  } catch (error) {
    return { error: { message: 'Network error occurred' }, data: null };
  }
}

// Sign up function
export async function signUp(credentials: { email: string; password: string; name?: string }) {
  try {
    const response = await fetch('/api/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    const data = await response.json();

    if (response.ok) {
      // Store the JWT token in a cookie if returned
      if (data.token) {
        const expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate() + 1); // 1 day from now

        // Create cookie string without using template literals or regex-sensitive characters
        const cookieParts = [
          'auth_token=' + data.token,
          'path=/',
          'expires=' + expirationDate.toUTCString(),
          'SameSite=Lax'
        ];
        document.cookie = cookieParts.join('; ');
      }

      return { error: null, data };
    } else {
      return { error: { message: data.error || 'Signup failed' }, data: null };
    }
  } catch (error) {
    return { error: { message: 'Network error occurred' }, data: null };
  }
}

// Sign out function
export async function signOut(options?: { callbackURL?: string }) {
  // Remove the auth token from cookies
  document.cookie = 'auth_token=; Max-Age=0; path=/;';

  // Redirect if callbackURL is provided
  if (options?.callbackURL) {
    window.location.href = options.callbackURL || '/login';
  } else {
    window.location.href = '/login';
  }
}

// Get JWT token
export function getJwt() {
  if (typeof window !== 'undefined') {
    const cookies = document.cookie.split('; ');
    for (let i = 0; i < cookies.length; i++) {
      if (cookies[i].startsWith('auth_token=')) {
        const parts = cookies[i].split('=');
        return parts[1];
      }
    }
  }
  return null;
}

// Export a mock client object for compatibility
export const authClient = {
  signIn: {
    email: (credentials: { email: string; password: string }, options?: { callbackURL?: string }) => signIn(credentials, options)
  },
  signUp: {
    email: (credentials: { email: string; password: string; name?: string }) => signUp(credentials)
  },
  signOut,
  useSession,
  getJwt,
  Provider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
};