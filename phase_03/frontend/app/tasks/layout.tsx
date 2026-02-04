'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Sidebar from '../../components/Sidebar';

export default function TasksLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, loading, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Check authentication status after initial loading
    if (!loading) {
      if (!isAuthenticated()) {
        // Redirect to login if not authenticated
        router.push('/login');
        router.refresh();
      }
    }
  }, [user, loading, isAuthenticated, router]);

  // Show loading state while checking auth
  if (loading || (!loading && !isAuthenticated())) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="max-w-md w-full space-y-8 text-center">
          {loading ? (
            <h2 className="text-2xl font-bold text-gray-200">Loading...</h2>
          ) : (
            <>
              <h2 className="text-2xl font-bold text-gray-200">Please log in</h2>
              <p className="text-gray-400">You need to be logged in to access your tasks</p>
            </>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 md:ml-64 transition-all duration-300">
        {children}
      </main>
    </div>
  );
}