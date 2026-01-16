"use client";

import { AuthProvider as CustomAuthProviderImpl } from "@/lib/auth-context";

export function AuthProviderWrapper({ children }: { children: React.ReactNode }) {
  return <CustomAuthProviderImpl>{children}</CustomAuthProviderImpl>;
}