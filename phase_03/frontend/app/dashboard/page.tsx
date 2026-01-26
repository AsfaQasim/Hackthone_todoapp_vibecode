'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import Sidebar from '../../components/Sidebar';
import ChatInterface from '../../components/ChatInterface';
import TaskForm from '../../components/TaskForm';
import TaskItem from '../../components/TaskItem';
import { Card, CardContent } from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import LoadingSpinner from '../../components/ui/LoadingSpinner';
import Skeleton from '../../components/ui/Skeleton';
import PageTransition from '../../components/PageTransition';

interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
}

export default function DashboardPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAddingTask, setIsAddingTask] = useState(false);
  const [deletingTaskId, setDeletingTaskId] = useState<number | null>(null);
  const [updatingTaskId, setUpdatingTaskId] = useState<number | null>(null);
  const [userId, setUserId] = useState<string | null>(null);
  const router = useRouter();

  // Function to fetch user info from backend if we can't decode the token
  const fetchUserInfo = async (token: string) => {
    try {
      const response = await fetch('http://localhost:8000/health', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        // For now, we'll just try to get user info from a potential user endpoint
        // This depends on your backend implementation
        console.log("Backend is reachable with the token");
      } else {
        console.error("Token not valid for backend");
        router.push('/login');
      }
    } catch (error) {
      console.error("Error verifying token with backend:", error);
    }
  };

  useEffect(() => {
    // Check if user is logged in by checking for auth token in cookies
    const tokenExists = document.cookie
      .split('; ')
      .find(row => row.startsWith('auth_token='));

    if (!tokenExists) {
      router.push('/login');
    } else {
      setIsLoggedIn(true);

      // Get user info from cookie or localStorage
      try {
        const userInfoStr = localStorage.getItem('user_info');
        if (userInfoStr) {
          const userInfo = JSON.parse(userInfoStr);
          setUserId(userInfo.id);
        } else {
          // If no user info in localStorage, try to decode the token to get user ID
          const cookies = document.cookie.split('; ');
          const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
          if (authTokenRow) {
            const token = authTokenRow.split('=')[1];
            // Decode JWT token to get user ID
            const tokenParts = token.split('.');
            if (tokenParts.length === 3) {
              try {
                // Add padding to base64 string if needed
                const base64Payload = tokenParts[1].replace(/-/g, '+').replace(/_/g, '/');
                const payload = JSON.parse(atob(base64Payload));
                setUserId(payload.sub || payload.userId || payload.id); // Try different possible fields
              } catch (e) {
                console.error('Error decoding token:', e);
                // If we can't decode the token, try to make a request to get user info
                fetchUserInfo(token);
              }
            }
          }
        }
      } catch (e) {
        console.error('Error parsing user info:', e);
      }

      loadTasks();
    }
  }, [router]);

  const loadTasks = async () => {
    try {
      setLoading(true);

      // Get the auth token from cookies
      const cookies = document.cookie.split('; ');
      const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
      const token = authTokenRow ? authTokenRow.split('=')[1] : null;

      if (!token) {
        router.push('/login');
        return;
      }

      const response = await fetch('/api/tasks', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.status === 401) {
        // Token expired or invalid, redirect to login
        router.push('/login');
        return;
      }

      if (!response.ok) {
        // Attempt to get error details from response
        let errorData;
        try {
          errorData = await response.json();
        } catch (parseError) {
          // If response is not JSON, get the text instead
          const errorText = await response.text();
          errorData = { error: errorText || `HTTP error! status: ${response.status}` };
        }

        console.error('Load tasks request failed:', errorData);
        throw new Error(errorData.error || `Failed to load tasks: ${response.status}`);
      }

      const data = await response.json();
      setTasks(data);
    } catch (error: any) {
      console.error('Error loading tasks:', error);
      setError(error.message || 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (title: string, description: string) => {
    setIsAddingTask(true);
    setError(null);

    if (!title.trim()) {
      setError('Task title is required');
      setIsAddingTask(false);
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
        body: JSON.stringify({
          title: title.trim(),
          description: description,
        }),
      });

      if (response.status === 401) {
        // Token expired or invalid, redirect to login
        router.push('/login');
        return;
      }

      if (!response.ok) {
        // Attempt to get error details from response
        let errorData;
        try {
          errorData = await response.json();
        } catch (parseError) {
          // If response is not JSON, get the text instead
          const errorText = await response.text();
          errorData = { error: errorText || `HTTP error! status: ${response.status}` };
        }

        console.error('Add task request failed:', errorData);
        throw new Error(errorData.error || `Failed to add task: ${response.status}`);
      }

      const newTask = await response.json();
      // Update the state immediately with the new task
      setTasks(prevTasks => [newTask, ...prevTasks]); // Add new task to the top of the list
    } catch (error: any) {
      console.error('Error adding task:', error);
      setError(error.message || 'Failed to add task');
    } finally {
      setIsAddingTask(false);
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    try {
      // Get the auth token from cookies
      const cookies = document.cookie.split('; ');
      const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
      const token = authTokenRow ? authTokenRow.split('=')[1] : null;

      if (!token) {
        router.push('/login');
        return;
      }

      // Find the current task
      const currentTask = tasks.find(t => t.id === taskId);
      if (!currentTask) return;

      // Optimistically update the UI
      setTasks(prevTasks => prevTasks.map(task =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      ));

      setUpdatingTaskId(taskId);

      // Make API call to update the task status
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          completed: !currentTask.completed
        }),
      });

      if (response.status === 401) {
        // Token expired or invalid, redirect to login
        router.push('/login');
        return;
      }

      if (!response.ok) {
        // Attempt to get error details from response
        let errorData;
        try {
          errorData = await response.json();
        } catch (parseError) {
          // If response is not JSON, get the text instead
          const errorText = await response.text();
          errorData = { error: errorText || `HTTP error! status: ${response.status}` };
        }

        console.error('Update task request failed:', errorData);
        throw new Error(errorData.error || `Failed to update task: ${response.status}`);
      }

      const updatedTask = await response.json();
      // Update the task in the state with the response
      setTasks(prevTasks => prevTasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (error: any) {
      console.error('Error toggling task completion:', error);
      // Revert the optimistic update on error
      setTasks(prevTasks => prevTasks.map(task =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      ));
      setError(error.message || 'Failed to update task');
    } finally {
      setUpdatingTaskId(null);
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    // Validate the task ID before making the request
    if (!taskId || isNaN(Number(taskId))) {
      console.error('Invalid task ID provided:', taskId);
      setError('Invalid task ID');
      setDeletingTaskId(null);
      return;
    }

    setDeletingTaskId(taskId);

    try {
      // Get the auth token from cookies
      const cookies = document.cookie.split('; ');
      const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
      const token = authTokenRow ? authTokenRow.split('=')[1] : null;

      if (!token) {
        console.log('No auth token found in cookies');
        router.push('/login');
        return;
      }

      console.log('Sending delete request for task ID:', taskId);
      console.log('Auth token:', token.substring(0, 10) + '...');

      const response = await fetch(`/api/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      console.log('Delete response status:', response.status);

      if (response.status === 401) {
        // Token expired or invalid, redirect to login
        router.push('/login');
        return;
      }

      if (!response.ok) {
        // Attempt to get error details from response
        let errorData;
        try {
          errorData = await response.json();
        } catch (parseError) {
          // If response is not JSON, get the text instead
          const errorText = await response.text();
          errorData = { error: errorText || `HTTP error! status: ${response.status}` };
        }

        console.error('Delete request failed:', errorData);
        throw new Error(errorData.error || `Failed to delete task: ${response.status}`);
      }

      // For successful deletion, the API returns JSON with a message
      // We can optionally process it, but the main thing is removing from UI
      const result = await response.json();
      console.log(result.message); // Log success message

      // Remove the task from the UI
      setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
    } catch (error: any) {
      console.error('Error deleting task:', error);
      setError(error.message || 'Failed to delete task');
    } finally {
      setDeletingTaskId(null);
    }
  };

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="max-w-md w-full space-y-8 text-center">
          <h2 className="text-2xl font-bold text-gray-200">Please log in</h2>
          <p className="text-gray-400">You need to be logged in to access your dashboard</p>
          <button
            onClick={() => router.push('/login')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  if (!userId) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="max-w-md w-full space-y-8 text-center">
          <h2 className="text-2xl font-bold text-gray-200">Loading...</h2>
          <p className="text-gray-400">Retrieving user information</p>
        </div>
      </div>
    );
  }

  return (
    <PageTransition>
      <div className="flex h-screen bg-gray-950">
        <Sidebar />
        <div className="flex-1 flex flex-col overflow-hidden">
          <header className="bg-gray-900 border-b border-gray-800 p-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                Dashboard
              </h1>
            </div>
          </header>

          <main className="flex-1 overflow-y-auto p-4 md:p-6">
            <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Tasks Section */}
              <div className="bg-gray-900/50 backdrop-blur-lg border border-gray-800 rounded-xl p-4">
                <motion.div
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  className="mb-6 text-center"
                >
                  <h2 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                    My Tasks
                  </h2>
                  <p className="text-gray-400 text-sm">Manage your daily tasks and boost productivity</p>
                </motion.div>

                {/* Error Message */}
                {error && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-4 rounded-lg bg-red-500/20 p-3 border border-red-500/30"
                  >
                    <div className="text-xs text-red-300">{error}</div>
                  </motion.div>
                )}

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                >
                  <TaskForm onAddTask={handleAddTask} isLoading={isAddingTask} />
                </motion.div>

                {/* Tasks Section */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="mt-6"
                >
                  <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
                    <h3 className="text-lg font-semibold text-white">Your Tasks</h3>
                    <span className="text-gray-400 text-sm">
                      {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
                    </span>
                  </div>

                  {loading ? (
                    <div className="space-y-3 max-h-60 overflow-y-auto pr-2">
                      {[...Array(3)].map((_, index) => (
                        <Skeleton key={index} className="h-16 w-full" />
                      ))}
                    </div>
                  ) : tasks.length === 0 ? (
                    <Card className="text-center py-8">
                      <CardContent>
                        <div className="text-gray-400 mb-2">No tasks yet</div>
                        <p className="text-gray-500 text-sm">Add your first task to get started</p>
                      </CardContent>
                    </Card>
                  ) : (
                    <div className="space-y-3 max-h-60 overflow-y-auto pr-2">
                      {tasks.map((task) => (
                        <TaskItem
                          key={task.id}
                          task={task}
                          onToggleComplete={handleToggleComplete}
                          onDelete={handleDeleteTask}
                          isUpdating={updatingTaskId === task.id}
                          isDeleting={deletingTaskId === task.id}
                        />
                      ))}
                    </div>
                  )}
                </motion.div>
              </div>

              {/* Chat Section */}
              <div>
                <motion.div
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  className="mb-6 text-center"
                >
                  <h2 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                    AI Task Assistant
                  </h2>
                  <p className="text-gray-400 text-sm">Chat with your AI assistant to manage tasks</p>
                </motion.div>

                <ChatInterface userId={userId} />
              </div>
            </div>
          </main>
        </div>
      </div>
    </PageTransition>
  );
}