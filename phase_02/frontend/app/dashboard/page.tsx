'use client';

import { useSession } from 'better-auth/react';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function DashboardPage() {
  const { data: session, isPending } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (!isPending && !session) {
      router.push('/'); // Redirect to home if not authenticated
    }
  }, [session, isPending, router]);

  if (isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-lg text-gray-600">Loading...</p>
      </div>
    );
  }

  if (!session) {
    return null; // Redirect happens in useEffect
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow rounded-lg p-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="border rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-2">User Information</h2>
              <p><span className="font-medium">Name:</span> {session.user.name || 'N/A'}</p>
              <p><span className="font-medium">Email:</span> {session.user.email}</p>
              <p><span className="font-medium">Account ID:</span> {session.user.id}</p>
            </div>
            
            <div className="border rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-2">Quick Actions</h2>
              <ul className="space-y-2">
                <li>
                  <Link href="/todos" className="text-indigo-600 hover:text-indigo-800">
                    Manage Todos
                  </Link>
                </li>
                <li>
                  <Link href="/profile" className="text-indigo-600 hover:text-indigo-800">
                    Profile Settings
                  </Link>
                </li>
                <li>
                  <Link href="/settings" className="text-indigo-600 hover:text-indigo-800">
                    Account Settings
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Activity</h2>
            <div className="bg-gray-50 rounded-lg p-4">
              <p>No recent activity yet. Start by creating some todos!</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}