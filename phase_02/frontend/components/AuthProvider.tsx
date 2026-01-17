'use client';

import { AuthProvider as BetterAuthProvider } from 'better-auth/react';
import { authClient } from '../lib/auth-client';
import { ReactNode } from 'react';

export default function AuthProvider({ children }: { children: ReactNode }) {
  return (
    <BetterAuthProvider
      client={authClient}
      baseURL={process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000'}
    >
      {children}
    </BetterAuthProvider>
  );
}