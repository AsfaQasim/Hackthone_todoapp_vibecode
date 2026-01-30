'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';

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

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Check for existing session on initial load
  useEffect(() => {
    const checkExistingSession = async () => {
      console.log('Checking existing session...'); // Debug log
      try {
        // Check if we're in the browser (not during SSR)
        if (typeof window !== 'undefined') {
          // Check for auth token in cookies
          const cookies = document.cookie.split('; ');
          console.log('Cookies found:', cookies.length); // Debug log

          const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
          console.log('Auth token row found:', !!authTokenRow); // Debug log

          if (authTokenRow) {
            const token = authTokenRow.split('=')[1];
            console.log('Token found, length:', token.length); // Debug log

            // Decode JWT token to get user info
            const tokenParts = token.split('.');
            if (tokenParts.length === 3) {
              try {
                // Add padding to base64 string if needed
                let base64Payload = tokenParts[1];
                while (base64Payload.length % 4) {
                  base64Payload += '=';
                }
                const payload = JSON.parse(atob(base64Payload));
                console.log('Decoded payload:', payload); // Debug log

                // Create user object from token payload
                const userInfo: User = {
                  id: payload.sub || payload.userId || payload.user_id || payload.id || 'unknown',
                  email: payload.email || 'unknown@example.com',
                  name: payload.name || payload.full_name,
                };

                setUser(userInfo);
              } catch (e) {
                console.error('Error decoding token:', e);
                // If token decoding fails, we still have a token but can't parse user info
                // So we'll set a minimal user object
                setUser({
                  id: 'unknown',
                  email: 'unknown@example.com',
                });
              }
            }
          } else {
            console.log('No auth token found in cookies'); // Debug log
          }
        } else {
          console.log('Not in browser, skipping session check'); // Debug log
        }
        // If no token is found, user remains null, which is fine
      } catch (error) {
        console.error('Error checking existing session:', error);
      } finally {
        console.log('Setting loading to false'); // Debug log
        // Always set loading to false after checking session
        setLoading(false);
      }
    };

    checkExistingSession();
  }, []); // Empty dependency array to run only once on mount

  const login = async (email: string, password: string): Promise<boolean> => {
    console.log('Starting login process...'); // Debug log
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      // The API route sets the cookie automatically, so we don't need to manually set it
      const data = await response.json();
      console.log('Login response:', response.status, data); // Debug log

      if (response.ok) {
        // Decode token to get user info
        // Get the token from the response for user info, but rely on cookie for auth state
        if (data.token) {
          const tokenParts = data.token.split('.');
          if (tokenParts.length === 3) {
            try {
              let base64Payload = tokenParts[1];
              while (base64Payload.length % 4) {
                base64Payload += '=';
              }
              const payload = JSON.parse(atob(base64Payload));
              console.log('Login - decoded payload:', payload); // Debug log

              const userInfo: User = {
                id: payload.sub || payload.userId || payload.user_id || payload.id || 'unknown',
                email: payload.email || email,
                name: payload.name || payload.full_name,
              };

              setUser(userInfo);
              return true;
            } catch (e) {
              console.error('Error decoding token:', e);
              // Create a minimal user object if token decoding fails
              setUser({
                id: 'unknown',
                email: email,
              });
              return true;
            }
          }
        }
        // If no token in response but request was successful,
        // the cookie was set and we can still return true
        return true;
      } else {
        console.error('Login failed:', data.error || 'Unknown error');
        return false;
      }
    } catch (error) {
      console.error('Network error during login:', error);
      return false;
    }
  };

  const signup = async (email: string, password: string, name?: string): Promise<boolean> => {
    console.log('Starting signup process...'); // Debug log
    try {
      const response = await fetch('/api/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      // The API route sets the cookie automatically after successful signup
      const data = await response.json();
      console.log('Signup response:', response.status, data); // Debug log

      if (response.ok) {
        // Decode token to get user info
        if (data.token) {
          const tokenParts = data.token.split('.');
          if (tokenParts.length === 3) {
            try {
              let base64Payload = tokenParts[1];
              while (base64Payload.length % 4) {
                base64Payload += '=';
              }
              const payload = JSON.parse(atob(base64Payload));
              console.log('Signup - decoded payload:', payload); // Debug log

              const userInfo: User = {
                id: payload.sub || payload.userId || payload.user_id || payload.id || 'unknown',
                email: payload.email || email,
                name: payload.name || payload.full_name || name,
              };

              setUser(userInfo);
              return true;
            } catch (e) {
              console.error('Error decoding token:', e);
              // Create a minimal user object if token decoding fails
              setUser({
                id: 'unknown',
                email: email,
                name: name,
              });
              return true;
            }
          }
        }
        // If no token in response but request was successful,
        // the cookie was set and we can still return true
        return true;
      } else {
        console.error('Signup failed:', data.error || 'Unknown error');
        return false;
      }
    } catch (error) {
      console.error('Network error during signup:', error);
      return false;
    }
  };

  const logout = () => {
    // Remove the auth token from cookies
    document.cookie = 'auth_token=; Max-Age=0; path=/; domain=; secure=false; samesite=lax';

    // Clear any user data from localStorage
    localStorage.removeItem('user_info');

    setUser(null);
  };

  const isAuthenticated = (): boolean => {
    return !!user;
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