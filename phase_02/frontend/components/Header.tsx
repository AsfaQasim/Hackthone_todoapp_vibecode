"use client";

import Link from 'next/link';
import { useSession } from '../lib/auth-client';
import { useAtomValue } from 'jotai';
import LogoutButton from './LogoutButton';

export default function Header() {
    const sessionData = useAtomValue(useSession);
    const { data: session, isPending } = sessionData;

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <Link href="/" className="text-xl font-bold text-indigo-600">
                Todo App
              </Link>
            </div>
            <nav className="ml-6 flex space-x-8">
              <Link
                href="/"
                className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300"
              >
                Home
              </Link>
              {session && (
                <>
                  <Link
                    href="/dashboard"
                    className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300"
                  >
                    Dashboard
                  </Link>
                  <Link
                    href="/todos"
                    className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300"
                  >
                    My Todos
                  </Link>
                </>
              )}
            </nav>
          </div>
          <div className="flex items-center">
            {isPending ? (
              <div>Loading...</div>
            ) : session ? (
              <div className="flex items-center">
                <span className="mr-4 text-sm text-gray-700">Welcome, {session.user?.name || session.user?.email}</span>
                <LogoutButton />
              </div>
            ) : (
              <Link
                href="/login"
                className="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Sign In
              </Link>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}