"use client";

import { PropsWithChildren } from "react";

// Better Auth client provider wrapper
// Temporary workaround: Since the Provider is not properly initialized,
// we'll just return the children directly
const AuthProvider = ({ children }: PropsWithChildren) => {
  // For now, just return children without any provider
  // This avoids the error while we resolve the underlying issue
  return <>{children}</>;
};

export default AuthProvider;