'use client';

import { Provider } from 'better-auth/react';
import { authClient } from '../lib/auth-client';
import { ReactNode } from 'react';

export default function AuthProvider({ children }: { children: ReactNode }) {
  return (
    <Provider client={authClient}>
      {children}
    </Provider>
  );
}