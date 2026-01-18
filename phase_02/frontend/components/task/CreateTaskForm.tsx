'use client';

import { useState } from 'react';
import { useSession } from '../../lib/auth-client';
import { Task } from '@/types/task';
import { apiCall } from '../../lib/api';

interface CreateTaskFormProps {
  onTaskCreated: (task: Task) => void;
}

export default function CreateTaskForm({ onTaskCreated }: CreateTaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { data: session, isPending } = useSession();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    if (!title.trim()) {
      setError('Title is required');
      setLoading(false);
      return;
    }

    if (!session?.user?.id) {
      setError('User not authenticated');
      setLoading(false);
      return;
    }

    try {
      const newTask = await apiCall<Task>('/api/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim(),
        }),
      });

      onTaskCreated(newTask);
      setTitle('');
      setDescription('');
    } catch (err) {
      console.error('Error creating task:', err);
      setError('Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-6 p-4 bg-white rounded-lg border border-gray-200">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Create New Task</h2>
      
      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Enter task title"
            disabled={loading}
          />
        </div>
        
        <div className="mb-4">
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Enter task description (optional)"
            rows={3}
            disabled={loading}
          />
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className={`px-4 py-2 bg-indigo-600 text-white rounded-md font-medium ${
            loading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-indigo-700'
          }`}
        >
          {loading ? 'Creating...' : 'Create Task'}
        </button>
      </form>
    </div>
  );
}