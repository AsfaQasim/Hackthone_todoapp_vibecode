'use client';

import Link from 'next/link';

export default function HomePageWrapper() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
            <span className="block">Secure Todo Management</span>
            <span className="block text-indigo-600 mt-2">Organize your tasks safely</span>
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            A secure, user-isolated todo application with JWT-based authentication.
          </p>
        </div>

        <div className="mt-12 max-w-3xl mx-auto">
          <div className="bg-white rounded-lg shadow-xl overflow-hidden">
            <div className="px-6 py-8 sm:p-10">
              <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Demo Authentication System</h2>
                <p className="text-gray-600 mb-6">Login or signup to access the demo</p>
                <div className="space-y-4">
                  <Link
                    href="/login"
                    className="inline-block px-6 py-3 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 transition-colors"
                  >
                    Login
                  </Link>
                  <Link
                    href="/signup"
                    className="inline-block ml-4 px-6 py-3 bg-white text-indigo-600 font-medium rounded-md border border-indigo-600 hover:bg-indigo-50 transition-colors"
                  >
                    Sign Up
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function HomePageWithProvider() {
  return <HomePageWrapper />;
}