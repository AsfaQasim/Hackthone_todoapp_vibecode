'use client';

import { useEffect } from 'react';
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

  useEffect(() => {
    if (!loading && !user) {
      // User is not authenticated, redirect to login
      router.replace('/login');
    }
  }, [user, loading, router]);

  // Show nothing while checking auth status
  if (loading || (!user && !loading)) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="max-w-md w-full space-y-8 text-center">
          <h2 className="text-2xl font-bold text-gray-200">Loading...</h2>
          <p className="text-gray-400">Verifying your session</p>
        </div>
      </div>
    );
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

  useEffect(() => {
    if (!loading && user) {
      // User is authenticated, redirect to dashboard
      router.replace('/dashboard');
    }
  }, [user, loading, router]);

  // Show nothing while checking auth status
  if (loading || (user && !loading)) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="max-w-md w-full space-y-8 text-center">
          <h2 className="text-2xl font-bold text-gray-200">Loading...</h2>
          <p className="text-gray-400">Redirecting...</p>
        </div>
      </div>
    );
  }

  // User is not authenticated, show the guest-only content
  return <>{children}</>;
};