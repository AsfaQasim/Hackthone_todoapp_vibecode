'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import ChatInterface from '../../components/ChatInterface';
import PageTransition from '../../components/PageTransition';
import { useAuth } from '../../contexts/AuthContext';
import { ProtectedRoute } from '../../components/RouteProtector';

export default function ChatPage() {
  const { user } = useAuth();

  return (
    <ProtectedRoute>
      <PageTransition>
        <div className="flex-1 flex flex-col overflow-hidden">
          <header className="bg-gray-900 border-b border-gray-800 p-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                AI Task Assistant
              </h1>
            </div>
          </header>

          <main className="flex-1 overflow-y-auto p-4 md:p-6">
            <div className="max-w-4xl mx-auto">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <ChatInterface userId={user?.id || ''} />
              </motion.div>
            </div>
          </main>
        </div>
      </PageTransition>
    </ProtectedRoute>
  );
}