'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../contexts/AuthContext';
import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';

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
      console.log('🔒 ProtectedRoute: No user found, redirecting to login');
      router.replace('/login');
    }
  }, [user, loading, router]);

  // Show loading spinner while checking auth status
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-gray-800">
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="mx-auto mb-4"
          >
            <Sparkles className="h-12 w-12 text-cyan-400" />
          </motion.div>
          <p className="text-gray-300 text-lg">Loading...</p>
        </div>
      </div>
    );
  }

  // If user is not authenticated after loading completes, show loading while redirecting
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-gray-800">
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="mx-auto mb-4"
          >
            <Sparkles className="h-12 w-12 text-cyan-400" />
          </motion.div>
          <p className="text-gray-300 text-lg">Redirecting to login...</p>
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

  // Redirect after render when conditions are met
  React.useEffect(() => {
    if (!loading && user) {
      console.log('👤 GuestOnlyRoute: User found, redirecting to dashboard');
      router.replace('/dashboard');
    }
  }, [user, loading, router]);

  // Show loading spinner while checking auth status
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-gray-800">
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="mx-auto mb-4"
          >
            <Sparkles className="h-12 w-12 text-cyan-400" />
          </motion.div>
          <p className="text-gray-300 text-lg">Loading...</p>
        </div>
      </div>
    );
  }

  // If user is authenticated after loading completes, show loading while redirecting
  if (user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-gray-800">
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="mx-auto mb-4"
          >
            <Sparkles className="h-12 w-12 text-cyan-400" />
          </motion.div>
          <p className="text-gray-300 text-lg">Redirecting to dashboard...</p>
        </div>
      </div>
    );
  }

  // User is not authenticated, show the guest-only content
  return <>{children}</>;
};