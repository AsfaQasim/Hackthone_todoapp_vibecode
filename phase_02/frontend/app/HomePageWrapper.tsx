'use client';

import { useSession } from '../lib/auth-client';
import { useAtomValue } from 'jotai';
import Link from 'next/link';
import AuthComponent from '../components/AuthComponent';

export default function HomePageWrapper() {
  const sessionData = useAtomValue(useSession);
  const { data: session, isPending } = sessionData;

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
          {isPending ? (
            <div className="text-center py-10">
              <p className="text-lg text-gray-600">Loading...</p>
            </div>
          ) : session ? (
            <div className="bg-white rounded-lg shadow-xl p-8 text-center">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Welcome back, {session.user.name || session.user.email}!</h2>
              <p className="text-gray-600 mb-6">Ready to manage your tasks?</p>
              <div className="space-y-4">
                <Link
                  href="/dashboard"
                  className="inline-block px-6 py-3 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 transition-colors"
                >
                  Go to Dashboard
                </Link>
                <Link
                  href="/todos"
                  className="inline-block ml-4 px-6 py-3 bg-white text-indigo-600 font-medium rounded-md border border-indigo-600 hover:bg-indigo-50 transition-colors"
                >
                  View My Todos
                </Link>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow-xl overflow-hidden">
              <div className="px-6 py-8 sm:p-10">
                <AuthComponent onAuthSuccess={() => window.location.reload()} />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export function HomePageWithProvider() {
  return <HomePageWrapper />;
}