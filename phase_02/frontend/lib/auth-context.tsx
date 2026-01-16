import { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
import { authClient } from './auth-client';

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  signIn: (email: string, password: string) => Promise<boolean>;
  signUp: (email: string, password: string, name: string) => Promise<boolean>;
  signOut: () => Promise<void>;
  getSession: () => Promise<any | null>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Initialize user session
  useEffect(() => {
    const initializeSession = async () => {
      try {
        const session = await authClient.getSession();
        if (session?.data?.user) {
          setUser({
            id: session.data.user.id,
            email: session.data.user.email,
            name: session.data.user.name || session.data.user.email.split('@')[0]
          });
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Error initializing session:', error);
      } finally {
        setLoading(false);
      }
    };

    initializeSession();
  }, []);

  const signIn = useCallback(async (email: string, password: string): Promise<boolean> => {
    try {
      const result = await authClient.signIn(email, password);
      if (result) {
        setUser({
          id: result.user.id,
          email: result.user.email,
          name: result.user.name || result.user.email.split('@')[0]
        });
        setIsAuthenticated(true);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Sign in error:', error);
      return false;
    }
  }, []);

  const signUp = useCallback(async (email: string, password: string, name: string): Promise<boolean> => {
    try {
      const result = await authClient.signUp(email, password, name);
      if (result) {
        setUser({
          id: result.user.id,
          email: result.user.email,
          name: result.user.name || result.user.email.split('@')[0]
        });
        setIsAuthenticated(true);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Sign up error:', error);
      return false;
    }
  }, []);

  const signOut = useCallback(async () => {
    try {
      await authClient.signOut();
      setUser(null);
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Sign out error:', error);
      // Still clear local state even if API call fails
      setUser(null);
      setIsAuthenticated(false);
    }
  }, []);

  const getSession = async () => {
    try {
      return await authClient.getSession();
    } catch (error) {
      console.error('Get session error:', error);
      return null;
    }
  };

  return (
    <AuthContext.Provider value={{
      user,
      loading,
      isAuthenticated,
      signIn,
      signUp,
      signOut,
      getSession
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}