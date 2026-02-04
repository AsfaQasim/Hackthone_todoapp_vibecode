'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authClient, signIn as signInFn, signUp as signUpFn } from '../lib/auth-client';

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  signup: (email: string, password: string, name?: string) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

// Helper function to decode JWT token and extract user info
const decodeToken = (token: string): { sub: string; email: string; name?: string } | null => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return {
      sub: payload.sub || '',
      email: payload.email || '',
      name: payload.name || payload.email?.split('@')[0] || ''
    };
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

// Helper function to get token from cookies
const getTokenFromCookies = (): string | null => {
  if (typeof window !== 'undefined') {
    const cookies = document.cookie.split('; ');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith('auth_token=')) {
        return cookie.substring('auth_token='.length);
      }
    }
  }
  return null;
};

// Helper function to remove token from cookies
const removeTokenFromCookies = (): void => {
  if (typeof window !== 'undefined') {
    document.cookie = 'auth_token=; Max-Age=0; path=/; domain=' + window.location.hostname + ';';
    // Also try without domain for localhost
    document.cookie = 'auth_token=; Max-Age=0; path=/;';
  }
};

// Helper function to save token to cookies
const saveTokenToCookies = (token: string): void => {
  if (typeof window !== 'undefined') {
    // Set the cookie with a 7-day expiration
    const expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + 7);

    document.cookie = `auth_token=${token}; expires=${expirationDate.toUTCString()}; path=/; SameSite=Strict`;
  }
};

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Initialize auth state on component mount
  useEffect(() => {
    const initAuthState = () => {
      try {
        // Get token from cookies
        const token = getTokenFromCookies();

        if (token) {
          // Decode token to get user info
          const decoded = decodeToken(token);

          if (decoded) {
            setUser({
              id: decoded.sub,
              email: decoded.email,
              name: decoded.name
            });
          } else {
            // Token is invalid, remove it
            removeTokenFromCookies();
          }
        }
      } catch (error) {
        console.error('Error initializing auth state:', error);
        // Clear any potentially corrupted token
        removeTokenFromCookies();
      } finally {
        setLoading(false);
      }
    };

    // Use setTimeout to defer initialization to avoid hydration issues
    const timer = setTimeout(initAuthState, 0);

    return () => clearTimeout(timer);
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      console.log('Attempting login with email:', email);

      // Call the login API
      const result = await signInFn({ email, password });
      console.log('Login API result:', result);

      if (result.error) {
        console.error('Login API error:', result.error.message);
        return false;
      }

      // Check if we received a token in the response
      if (result.data && result.data.access_token) {
        // Save the token to cookies
        saveTokenToCookies(result.data.access_token);

        // Decode the token to get user info
        const decoded = decodeToken(result.data.access_token);

        if (decoded) {
          // Set user state immediately
          setUser({
            id: decoded.sub,
            email: decoded.email,
            name: decoded.name
          });

          console.log('Login successful, user set:', decoded);
          return true;
        } else {
          console.error('Could not decode token after login');
          return false;
        }
      } else {
        console.error('No access_token in login response');
        return false;
      }
    } catch (error) {
      console.error('Login exception:', error);
      return false;
    }
  };

  const signup = async (email: string, password: string, name?: string): Promise<boolean> => {
    try {
      console.log('Attempting signup with email:', email);

      const result = await signUpFn({
        email,
        password,
        name: name || email.split('@')[0],
      });
      console.log('Signup API result:', result);

      if (result.error) {
        console.error('Signup API error:', result.error.message);
        return false;
      }

      // Check if we received a token in the response
      if (result.data && result.data.access_token) {
        // Save the token to cookies
        saveTokenToCookies(result.data.access_token);

        // Decode the token to get user info
        const decoded = decodeToken(result.data.access_token);

        if (decoded) {
          // Set user state immediately
          setUser({
            id: decoded.sub,
            email: decoded.email,
            name: decoded.name
          });

          return true;
        } else {
          console.error('Could not decode token after signup');
          return false;
        }
      } else {
        console.error('No access_token in signup response');
        return false;
      }
    } catch (error) {
      console.error('Signup exception:', error);
      return false;
    }
  };

  const logout = () => {
    // Remove token from cookies
    removeTokenFromCookies();

    // Clear user state
    setUser(null);
  };

  const isAuthenticated = (): boolean => {
    return !!user && !loading;
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};