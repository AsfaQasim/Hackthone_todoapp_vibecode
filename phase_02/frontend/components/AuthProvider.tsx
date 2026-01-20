"use client";

import { PropsWithChildren } from "react";

// Better Auth doesn't require a top-level provider in many cases
// The hooks manage the authentication context automatically
export default function AuthProvider({ children }: PropsWithChildren) {
  return <>{children}</>;
}