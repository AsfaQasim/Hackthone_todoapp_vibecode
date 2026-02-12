'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function AddTaskPage() {
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      // Get the auth token from cookies
      const cookies = document.cookie.split('; ');
      const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
      const token = authTokenRow ? authTokenRow.split('=')[1] : null;

      if (!token) {
        router.push('/login');
        return;
      }

      const response = await fetch('/api/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ title: title.trim() }),
      });

      if (response.status === 401) {
        // Token expired or invalid, redirect to login
        router.push('/login');
        return;
      }

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || 'Failed to add task');
      }

      // On success, redirect back to tasks page
      router.push('/tasks');
      router.refresh(); // Refresh to show the new task
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 p-4">
      <div className="w-full max-w-md">
        <div className="bg-gray-800 rounded-lg shadow-lg p-6">
          <h1 className="text-2xl font-bold text-white mb-6 text-center">Add New Task</h1>

          {error && (
            <div className="mb-4 p-3 bg-red-500/20 text-red-300 rounded-md">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="title" className="block text-gray-300 mb-2">
                Title
              </label>
              <input
                id="title"
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
                placeholder="Enter task title"
              />
            </div>

            <button
              type="submit"
              className="w-full py-2 px-4 bg-cyan-600 hover:bg-cyan-700 text-white rounded-md transition duration-200"
            >
              Add Task
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}