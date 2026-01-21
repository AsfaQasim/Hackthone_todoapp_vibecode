'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function DashboardPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in by checking for auth token in cookies
    const tokenExists = document.cookie
      .split('; ')
      .find(row => row.startsWith('auth_token='));

    if (!tokenExists) {
      router.push('/login');
    } else {
      setIsLoggedIn(true);
    }
  }, [router]);

  const handleLogout = () => {
    // Remove the auth token from cookies
    document.cookie = 'auth_token=; Max-Age=0; path=/;';
    router.push('/login');
  };

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-xl text-center">
          <h2 className="text-2xl font-bold text-gray-800">Please log in</h2>
          <p className="text-gray-600">You need to be logged in to access the dashboard</p>
          <button
            onClick={() => router.push('/login')}
            className="inline-block px-6 py-3 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 transition-colors"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-xl p-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
            >
              Logout
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="border rounded-lg p-6 bg-gray-50">
              <h2 className="text-xl font-semibold text-gray-800 mb-2">Profile</h2>
              <p className="text-gray-600">Manage your account settings</p>
              <button className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
                Manage Profile
              </button>
            </div>

            <div className="border rounded-lg p-6 bg-gray-50">
              <h2 className="text-xl font-semibold text-gray-800 mb-2">Tasks</h2>
              <p className="text-gray-600">View and manage your tasks</p>
              <Link href="/tasks" className="mt-4 inline-block px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
                View Tasks
              </Link>
            </div>

            <div className="border rounded-lg p-6 bg-gray-50">
              <h2 className="text-xl font-semibold text-gray-800 mb-2">Settings</h2>
              <p className="text-gray-600">Configure application settings</p>
              <button className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
                Settings
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}