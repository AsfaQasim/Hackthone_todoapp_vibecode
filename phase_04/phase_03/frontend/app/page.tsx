'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { ArrowRight, CheckCircle, Zap, Shield } from 'lucide-react';
import PageTransition from '../components/PageTransition';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../contexts/AuthContext';

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-500 mx-auto"></div>
          <p className="mt-4 text-gray-300">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <PageTransition>
      <div className="min-h-screen flex flex-col relative overflow-hidden">
        {/* Background is handled by Layout component */}

        <div className="flex-grow flex items-center justify-center px-4 py-12 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="mb-10"
            >
              <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent mb-6">
                VibeCode Task Manager
              </h1>
              <p className="text-xl text-gray-300 max-w-2xl mx-auto mb-10">
                The premium task management solution designed for professionals who demand both beauty and functionality.
              </p>
            </motion.div>

            {user ? (
              // Show different content for logged-in users
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="flex flex-col sm:flex-row justify-center gap-4 mb-16"
              >
                <Link href="/dashboard" className="w-full sm:w-auto">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="w-full sm:w-auto px-6 py-3 sm:px-8 sm:py-4 bg-gradient-to-r from-cyan-600 to-blue-600 text-white font-medium rounded-xl hover:opacity-90 transition-opacity flex items-center justify-center text-sm sm:text-base"
                  >
                    Go to Dashboard
                    <ArrowRight className="ml-2 h-4 w-4 sm:h-5 sm:w-5" />
                  </motion.button>
                </Link>

                <Link href="/tasks" className="w-full sm:w-auto">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="w-full sm:w-auto px-6 py-3 sm:px-8 sm:py-4 bg-gray-800 text-white font-medium rounded-xl border border-gray-700 hover:bg-gray-700 transition-colors flex items-center justify-center text-sm sm:text-base"
                  >
                    Manage Tasks
                    <ArrowRight className="ml-2 h-4 w-4 sm:h-5 sm:w-5" />
                  </motion.button>
                </Link>
              </motion.div>
            ) : (
              // Show login/signup options for non-logged-in users
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="flex flex-col sm:flex-row justify-center gap-4 mb-16"
              >
                <Link href="/login" className="w-full sm:w-auto">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="w-full sm:w-auto px-6 py-3 sm:px-8 sm:py-4 bg-gradient-to-r from-cyan-600 to-blue-600 text-white font-medium rounded-xl hover:opacity-90 transition-opacity flex items-center justify-center text-sm sm:text-base"
                  >
                    Login to Dashboard
                    <ArrowRight className="ml-2 h-4 w-4 sm:h-5 sm:w-5" />
                  </motion.button>
                </Link>

                <Link href="/signup" className="w-full sm:w-auto">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="w-full sm:w-auto px-6 py-3 sm:px-8 sm:py-4 bg-gray-800 text-white font-medium rounded-xl border border-gray-700 hover:bg-gray-700 transition-colors flex items-center justify-center text-sm sm:text-base"
                  >
                    Create Account
                    <ArrowRight className="ml-2 h-4 w-4 sm:h-5 sm:w-5" />
                  </motion.button>
                </Link>
              </motion.div>
            )}

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto"
            >
              <div className="bg-gray-900/50 backdrop-blur-lg border border-gray-800 rounded-xl p-6">
                <div className="w-12 h-12 bg-cyan-900/30 rounded-lg flex items-center justify-center mb-4 mx-auto">
                  <Zap className="h-6 w-6 text-cyan-400" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">Lightning Fast</h3>
                <p className="text-gray-400">Optimized performance with instant task updates and real-time sync.</p>
              </div>

              <div className="bg-gray-900/50 backdrop-blur-lg border border-gray-800 rounded-xl p-6">
                <div className="w-12 h-12 bg-cyan-900/30 rounded-lg flex items-center justify-center mb-4 mx-auto">
                  <Shield className="h-6 w-6 text-cyan-400" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">Secure by Design</h3>
                <p className="text-gray-400">Enterprise-grade security with JWT authentication and encrypted data.</p>
              </div>

              <div className="bg-gray-900/50 backdrop-blur-lg border border-gray-800 rounded-xl p-6">
                <div className="w-12 h-12 bg-cyan-900/30 rounded-lg flex items-center justify-center mb-4 mx-auto">
                  <CheckCircle className="h-6 w-6 text-cyan-400" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">Always Synced</h3>
                <p className="text-gray-400">Access your tasks from anywhere with seamless cloud synchronization.</p>
              </div>
            </motion.div>
          </div>
        </div>

        <footer className="py-6 text-center text-gray-500 text-sm relative z-10">
          <p>© {new Date().getFullYear()} VibeCode. All rights reserved.</p>
        </footer>
      </div>
    </PageTransition>
  );
}