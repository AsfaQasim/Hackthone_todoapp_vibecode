'use client';

import { BaseProvider } from 'better-auth/client';
import { auth } from '../lib/auth-client';
import { ReactNode } from 'react';

export default function AuthProvider({ children }: { children: ReactNode }) {
  return <BaseProvider client={auth}>{children}</BaseProvider>;
}