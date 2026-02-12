'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../contexts/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

interface GuestOnlyRouteProps {
  children: React.ReactNode;
}

/**
 * Component that protects routes that require authentication
 * If user is not authenticated, redirects to login
 */
export const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const { user, loading } = useAuth();
  const router = useRouter();

  // Redirect after render when conditions are met
  React.useEffect(() => {
    if (!loading && !user) {
      router.replace('/login');
    }
  }, [user, loading, router]);

  // Don't render anything while loading or when redirect is needed
  if (loading) {
    return null; // Don't render anything while checking auth status
  }

  // If user is not authenticated after loading completes, return null (redirect will happen via useEffect)
  if (!user) {
    return null;
  }

  // User is authenticated, show the protected content
  return <>{children}</>;
};

/**
 * Component that restricts access to unauthenticated users only
 * If user is authenticated, redirects to dashboard
 */
export const GuestOnlyRoute = ({ children }: GuestOnlyRouteProps) => {
  const { user, loading } = useAuth();
  const router = useRouter();

  // Redirect after render when conditions are met
  React.useEffect(() => {
    if (!loading && user) {
      router.replace('/dashboard');
    }
  }, [user, loading, router]);

  // Don't render anything while loading or when redirect is needed
  if (loading) {
    return null; // Don't render anything while checking auth status
  }

  // If user is authenticated after loading completes, return null (redirect will happen via useEffect)
  if (user) {
    return null;
  }

  // User is not authenticated, show the guest-only content
  return <>{children}</>;
};