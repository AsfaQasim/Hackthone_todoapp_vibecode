'use client';

import { Suspense } from 'react';
import AuthProvider from '../components/AuthProvider';
import HomePageWrapper from './HomePageWrapper';

export default function Home() {
  return (
    <AuthProvider>
      <Suspense fallback={
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
              <div className="text-center py-10">
                <p className="text-lg text-gray-600">Loading...</p>
              </div>
            </div>
          </div>
        </div>
      }>
        <HomePageWrapper />
      </Suspense>
    </AuthProvider>
  );
}