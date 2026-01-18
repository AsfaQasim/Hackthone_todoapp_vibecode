'use client';

import { useState, useEffect } from 'react';
import { useSession } from '../../lib/auth-client';
import { useAtomValue } from 'jotai';
import { useRouter } from 'next/navigation';
import { Task } from '@/types/task';
import { apiCall } from '../../lib/api';
import CreateTaskForm from '../../components/task/CreateTaskForm';
import TaskItem from '../../components/task/TaskItem';

export default function TasksPage() {
  const sessionData = useAtomValue(useSession);
  const { data: session, isPending } = sessionData;
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isPending && !session) {
      // Redirect to login if not authenticated
      router.push('/signin');
    } else if (session) {
      fetchTasks();
    }
  }, [session, isPending, router]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      if (!session?.user?.id) {
        throw new Error('User ID not available');
      }

      const data = await apiCall<Task[]>(`/api/${session.user.id}/tasks`);
      setTasks(data);
    } catch (err) {
      console.error('Error fetching tasks:', err);
      setError('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskCreated = (newTask: Task) => {
    setTasks([newTask, ...tasks]);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (deletedTaskId: string) => {
    setTasks(tasks.filter(task => task.id !== deletedTaskId));
  };

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
          <h1 className="text-3xl font-bold text-gray-900 mb-6">My Tasks</h1>

          <CreateTaskForm onTaskCreated={handleTaskCreated} />

          {error && (
            <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          {loading ? (
            <div className="py-4 text-center">
              <p className="text-gray-600">Loading tasks...</p>
            </div>
          ) : tasks.length === 0 ? (
            <div className="py-8 text-center">
              <p className="text-gray-600">No tasks yet. Create one above!</p>
            </div>
          ) : (
            <div>
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Your Tasks ({tasks.length})
              </h2>
              <div className="space-y-2">
                {tasks.map(task => (
                  <TaskItem
                    key={task.id}
                    task={task}
                    onUpdate={handleTaskUpdated}
                    onDelete={handleTaskDeleted}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}