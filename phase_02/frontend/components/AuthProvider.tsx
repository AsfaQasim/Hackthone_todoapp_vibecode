'use client';

import { createContext, useContext, ReactNode } from 'react';
import { auth } from '../lib/auth-client';

// Create a context to provide the auth client to child components
const AuthContext = createContext(auth);

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default function AuthProvider({ children }: { children: ReactNode }) {
  return (
    <AuthContext.Provider value={auth}>
      {children}
    </AuthContext.Provider>
  );
}