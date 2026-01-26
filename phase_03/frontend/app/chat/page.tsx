'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import Sidebar from '../../components/Sidebar';
import ChatInterface from '../../components/ChatInterface';
import PageTransition from '../../components/PageTransition';

export default function ChatPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);
  const router = useRouter();

  // Function to fetch user info from backend if we can't decode the token
  const fetchUserInfo = async (token: string) => {
    try {
      const response = await fetch('http://localhost:8000/health', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        console.log("Backend is reachable with the token");
      } else {
        console.error("Token not valid for backend");
        router.push('/login');
      }
    } catch (error) {
      console.error("Error verifying token with backend:", error);
    }
  };

  useEffect(() => {
    // Check if user is logged in by checking for auth token in cookies
    const tokenExists = document.cookie
      .split('; ')
      .find(row => row.startsWith('auth_token='));

    if (!tokenExists) {
      router.push('/login');
    } else {
      setIsLoggedIn(true);

      // Get user info from cookie or localStorage
      try {
        const userInfoStr = localStorage.getItem('user_info');
        if (userInfoStr) {
          const userInfo = JSON.parse(userInfoStr);
          setUserId(userInfo.id);
        } else {
          // If no user info in localStorage, try to decode the token to get user ID
          const cookies = document.cookie.split('; ');
          const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
          if (authTokenRow) {
            const token = authTokenRow.split('=')[1];
            // Decode JWT token to get user ID
            const tokenParts = token.split('.');
            if (tokenParts.length === 3) {
              try {
                // Add padding to base64 string if needed
                const base64Payload = tokenParts[1].replace(/-/g, '+').replace(/_/g, '/');
                const payload = JSON.parse(atob(base64Payload));
                setUserId(payload.sub || payload.userId || payload.id); // Try different possible fields
              } catch (e) {
                console.error('Error decoding token:', e);
                // If we can't decode the token, try to make a request to get user info
                fetchUserInfo(token);
              }
            }
          }
        }
      } catch (e) {
        console.error('Error parsing user info:', e);
      }
    }
  }, [router]);

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="max-w-md w-full space-y-8 text-center">
          <h2 className="text-2xl font-bold text-gray-200">Please log in</h2>
          <p className="text-gray-400">You need to be logged in to access the chat</p>
          <button
            onClick={() => router.push('/login')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  if (!userId) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="max-w-md w-full space-y-8 text-center">
          <h2 className="text-2xl font-bold text-gray-200">Loading...</h2>
          <p className="text-gray-400">Retrieving user information</p>
        </div>
      </div>
    );
  }

  return (
    <PageTransition>
      <div className="flex h-screen bg-gray-950">
        <Sidebar />
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
                <ChatInterface userId={userId} />
              </motion.div>
            </div>
          </main>
        </div>
      </div>
    </PageTransition>
  );
}