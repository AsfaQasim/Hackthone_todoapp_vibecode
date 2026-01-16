'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '@/lib/auth-context';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export default function ProtectedRoute({ children, fallback = null }: ProtectedRouteProps) {
  const router = useRouter();
  const { loading, isAuthenticated } = useAuth();
  const [showFallback, setShowFallback] = useState(true);

  useEffect(() => {
    if (!loading) {
      if (!isAuthenticated) {
        // Redirect to login if not authenticated
        router.push('/auth/login');
      } else {
        // Show content if authenticated
        setShowFallback(false);
      }
    }
  }, [isAuthenticated, loading, router]);

  // Show fallback while checking authentication status
  if (loading || showFallback) {
    return fallback || (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // Render children if authenticated
  return <>{children}</>;
}