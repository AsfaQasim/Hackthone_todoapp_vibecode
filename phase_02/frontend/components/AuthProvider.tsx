"use client";

import { BetterAuthProvider } from "@better-auth/react";
import { auth } from "@/lib/auth";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  return <BetterAuthProvider client={auth}>{children}</BetterAuthProvider>;
}