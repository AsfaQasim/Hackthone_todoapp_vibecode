'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import Sidebar from '../../components/Sidebar';
import { Card, CardContent } from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import PageTransition from '../../components/PageTransition';
import { useAuth } from '../../contexts/AuthContext';

export default function ProfilePage() {
  const { user, loading, isAuthenticated } = useAuth();
  const router = useRouter();
  const [checkedAuth, setCheckedAuth] = useState(false);

  useEffect(() => {
    // Check authentication status after initial loading
    if (!loading) {
      if (!isAuthenticated()) {
        // Redirect to login if not authenticated
        router.push('/login');
        router.refresh();
      } else {
        // Auth is confirmed, allow rendering
        setCheckedAuth(true);
      }
    }
  }, [user, loading, isAuthenticated, router]);

  // Show loading state while checking auth
  if (loading || !checkedAuth) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="max-w-md w-full space-y-8 text-center">
          <h2 className="text-2xl font-bold text-gray-200">Loading...</h2>
          <p className="text-gray-400">Verifying your session</p>
        </div>
      </div>
    );
  }

  return (
    <PageTransition>
      <div className="flex min-h-screen">
        <Sidebar />
        
        <div className="flex-1 md:ml-64 transition-all duration-300">
          <div className="max-w-4xl mx-auto px-4 py-8">
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="mb-10 text-center"
            >
              <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                Profile
              </h1>
              <p className="text-gray-400 mt-2">Manage your account settings</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
            >
              <Card>
                <CardContent className="p-0">
                  <div className="p-6">
                    <div className="flex items-center mb-6">
                      <div className="bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16" />
                      <div className="ml-4">
                        <h2 className="text-xl font-semibold text-white">{user?.name || user?.email?.split('@')[0] || 'User'}</h2>
                        <p className="text-gray-400">{user?.email || 'Email not available'}</p>
                      </div>
                    </div>

                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">Email</label>
                        <input
                          type="email"
                          value={user?.email || ''}
                          readOnly
                          className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">Name</label>
                        <input
                          type="text"
                          value={user?.name || user?.email?.split('@')[0] || ''}
                          readOnly
                          className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white"
                        />
                      </div>
                    </div>

                    <div className="mt-6">
                      <Button variant="primary" className="w-full">
                        Update Profile
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </div>
    </PageTransition>
  );
}