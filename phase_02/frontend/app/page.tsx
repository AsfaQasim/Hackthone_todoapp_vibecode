"use client";

import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import AuthComponent from "@/components/AuthComponent";
import LogoutButton from "@/components/LogoutButton";
import { useEffect, useState } from "react";

export default function Home() {
  const { user, loading, isAuthenticated } = useAuth();
  const router = useRouter();
  const [serverStatus, setServerStatus] = useState<"checking" | "online" | "offline">("checking");

  useEffect(() => {
    const checkServerStatus = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/health`);
        if (response.ok) {
          setServerStatus("online");
        } else {
          setServerStatus("offline");
        }
      } catch (error) {
        setServerStatus("offline");
      }
    };

    checkServerStatus();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="mx-auto bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-4 rounded-2xl shadow-lg w-16 h-16 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h1 className="mt-4 text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            Todo Application
          </h1>
          <p className="mt-2 text-gray-600">Organize your tasks efficiently</p>

          {/* Server Status Indicator */}
          <div className={`mt-4 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
            serverStatus === "online"
              ? "bg-green-100 text-green-800"
              : serverStatus === "offline"
                ? "bg-red-100 text-red-800"
                : "bg-yellow-100 text-yellow-800"
          }`}>
            <span className={`mr-2 w-2 h-2 rounded-full ${
              serverStatus === "online"
                ? "bg-green-500"
                : serverStatus === "offline"
                  ? "bg-red-500"
                  : "bg-yellow-500"
              }`}></span>
            {serverStatus === "checking"
              ? "Checking server status..."
              : serverStatus === "online"
                ? "Server Online"
                : "Server Offline - Please start backend"}
          </div>
        </div>

        {isAuthenticated ? (
          <div className="mt-8 bg-white rounded-2xl shadow-xl p-8 border border-gray-200">
            <div className="text-center mb-6">
              <div className="mx-auto bg-green-100 text-green-800 rounded-full w-16 h-16 flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Welcome Back!</h2>
              <p className="mt-2 text-gray-600">
                Hi {user?.name || user?.email?.split('@')[0]}, you're signed in to your account.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-4">
              <button
                onClick={() => router.push('/dashboard')}
                className="w-full px-4 py-3 text-base font-semibold text-white bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shadow-md hover:shadow-lg transition-all duration-300 flex items-center justify-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                Go to Dashboard
              </button>

              <LogoutButton
                className="w-full px-4 py-3 text-base font-semibold text-white bg-gradient-to-r from-red-500 to-rose-600 rounded-lg hover:from-red-600 hover:to-rose-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 shadow-md hover:shadow-lg transition-all duration-300 flex items-center justify-center"
              />
            </div>
          </div>
        ) : (
          <div className="mt-8 bg-white rounded-2xl shadow-xl p-8 border border-gray-200">
            <p className="text-center text-gray-700 mb-6">Please sign in to access your tasks.</p>
            {serverStatus === "offline" && (
              <div className="mb-4 p-3 bg-red-50 rounded-lg border border-red-200">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">Backend Server Not Running</h3>
                    <div className="mt-2 text-sm text-red-700">
                      <p>Please start your backend server on http://localhost:8000 to enable authentication.</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div className="mt-4">
              <AuthComponent />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}