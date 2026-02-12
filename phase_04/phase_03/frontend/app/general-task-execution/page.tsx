'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent } from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import LoadingSpinner from '../../components/ui/LoadingSpinner';
import Skeleton from '../../components/ui/Skeleton';
import PageTransition from '../../components/PageTransition';
import { useAuth } from '../../contexts/AuthContext';
import { ProtectedRoute } from '../../components/RouteProtector';

interface Task {
  id: string;
  title: string;
  description: string;
  status: string;
  created_at: string;
  user_id: string;
}

export default function GeneralTaskExecutionPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load tasks when component mounts or user changes
  useEffect(() => {
    if (user) {
      console.log('Loading tasks for user:', user.email);
      loadTasks();
      
      // Auto-refresh every 5 seconds
      const interval = setInterval(() => {
        console.log('Auto-refreshing tasks...');
        loadTasks();
      }, 5000);
      
      return () => clearInterval(interval);
    }
  }, [user]);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      console.log('=== loadTasks called ===');

      // Get the auth token from cookies
      const cookies = document.cookie.split('; ');
      const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
      const token = authTokenRow ? authTokenRow.split('=')[1] : null;

      console.log('Auth token found:', !!token);

      if (!token) {
        setError('Authentication required. Please log in.');
        setLoading(false);
        return;
      }

      console.log('Fetching tasks from /api/tasks...');

      const response = await fetch('/api/tasks', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        cache: 'no-store', // Force fresh fetch
      });

      console.log('API response status:', response.status);

      if (response.status === 401) {
        setError('Authentication failed. Please log in again.');
        setLoading(false);
        return;
      }

      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
        } catch (parseError) {
          const errorText = await response.text();
          errorData = { error: errorText || `HTTP error! status: ${response.status}` };
        }

        console.error('Load tasks request failed:', errorData);
        throw new Error(errorData.error || `Failed to load tasks: ${response.status}`);
      }

      const data = await response.json();
      console.log('Tasks loaded:', data);
      
      setTasks(data);
    } catch (error: any) {
      console.error('Error loading tasks:', error);
      setError(error.message || 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      const cookies = document.cookie.split('; ');
      const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
      const token = authTokenRow ? authTokenRow.split('=')[1] : null;

      if (!token) {
        setError('Authentication required');
        return;
      }

      const response = await fetch(`/api/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to delete task');
      }
    } catch (error: any) {
      console.error('Error deleting task:', error);
      setError(error.message || 'Failed to delete task');
    }
  };

  const handleToggleComplete = async (taskId: string) => {
    try {
      const cookies = document.cookie.split('; ');
      const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
      const token = authTokenRow ? authTokenRow.split('=')[1] : null;

      if (!token) {
        setError('Authentication required');
        return;
      }

      const currentTask = tasks.find(t => t.id === taskId);
      if (!currentTask) return;

      const newStatus = currentTask.status === 'completed' ? 'pending' : 'completed';

      // Optimistically update UI
      setTasks(prevTasks => prevTasks.map(task =>
        task.id === taskId ? { ...task, status: newStatus } : task
      ));

      const response = await fetch(`/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          status: newStatus
        }),
      });

      if (!response.ok) {
        // Revert on error
        setTasks(prevTasks => prevTasks.map(task =>
          task.id === taskId ? { ...task, status: currentTask.status } : task
        ));
        const errorData = await response.json();
        setError(errorData.error || 'Failed to update task');
      }
    } catch (error: any) {
      console.error('Error updating task:', error);
      setError(error.message || 'Failed to update task');
    }
  };

  return (
    <ProtectedRoute>
      <PageTransition>
        <div className="max-w-full sm:max-w-md md:max-w-lg lg:max-w-4xl mx-auto px-4 py-6 sm:py-8">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-10 text-center"
          >
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
              AI Assistant Tasks
            </h1>
            <p className="text-gray-400 mt-2">Tasks created and managed by your AI assistant</p>
          </motion.div>

          {/* Debug Info */}
          <div className="mb-4 p-4 bg-gray-800 rounded-lg text-sm">
            <p className="text-gray-300">Debug Info:</p>
            <p className="text-gray-400">User: {user?.email || 'Not logged in'}</p>
            <p className="text-gray-400">Loading: {loading ? 'Yes' : 'No'}</p>
            <p className="text-gray-400">Tasks: {tasks.length}</p>
            {error && <p className="text-red-400">Error: {error}</p>}
          </div>

          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 rounded-lg bg-red-500/20 p-4 border border-red-500/30"
            >
              <div className="text-sm text-red-300">{error}</div>
              <Button
                onClick={loadTasks}
                className="mt-2 text-sm"
              >
                Retry
              </Button>
            </motion.div>
          )}

          {/* Tasks Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mt-10"
          >
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
              <h2 className="text-xl sm:text-2xl font-semibold text-white">Your AI Tasks</h2>
              <div className="flex items-center gap-4">
                <Button
                  onClick={loadTasks}
                  disabled={loading}
                  className="text-sm px-4 py-2"
                >
                  {loading ? 'Refreshing...' : '🔄 Refresh'}
                </Button>
                <span className="text-gray-400 text-sm sm:text-base">
                  {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
                </span>
              </div>
            </div>

            {loading ? (
              <div className="space-y-4 max-h-[50vh] overflow-y-auto pr-2 custom-scrollbar">
                {[...Array(3)].map((_, index) => (
                  <Skeleton key={index} className="h-20 w-full" />
                ))}
              </div>
            ) : tasks.length === 0 ? (
              <Card className="text-center py-12">
                <CardContent>
                  <div className="text-gray-400 mb-4">No AI tasks yet</div>
                  <p className="text-gray-500">Use the AI Assistant to create tasks</p>
                  <Button
                    onClick={() => window.location.href = '/chat'}
                    className="mt-4"
                  >
                    Go to AI Assistant
                  </Button>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4 max-h-[50vh] overflow-y-auto pr-2 custom-scrollbar">
                {tasks.map((task) => (
                  <Card key={task.id} className="hover:shadow-lg transition-shadow">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <h3 className={`text-lg font-semibold ${task.status === 'completed' ? 'line-through text-gray-500' : 'text-white'}`}>
                            {task.title}
                          </h3>
                          {task.description && (
                            <p className="text-gray-400 text-sm mt-1">{task.description}</p>
                          )}
                          <div className="flex items-center gap-4 mt-2">
                            <span className={`text-xs px-2 py-1 rounded ${
                              task.status === 'completed' 
                                ? 'bg-green-500/20 text-green-400' 
                                : 'bg-yellow-500/20 text-yellow-400'
                            }`}>
                              {task.status}
                            </span>
                            <span className="text-xs text-gray-500">
                              {new Date(task.created_at).toLocaleDateString()}
                            </span>
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <Button
                            onClick={() => handleToggleComplete(task.id)}
                            className="text-sm px-3 py-1"
                          >
                            {task.status === 'completed' ? 'Reopen' : 'Complete'}
                          </Button>
                          <Button
                            onClick={() => handleDeleteTask(task.id)}
                            className="text-sm px-3 py-1 bg-red-500 hover:bg-red-600"
                          >
                            Delete
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </motion.div>
        </div>
      </PageTransition>
    </ProtectedRoute>
  );
}
