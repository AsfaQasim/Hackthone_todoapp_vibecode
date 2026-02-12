'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import TaskForm from '../../components/TaskForm';
import TaskItem from '../../components/TaskItem';
import { Card, CardContent } from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import LoadingSpinner from '../../components/ui/LoadingSpinner';
import Skeleton from '../../components/ui/Skeleton';
import PageTransition from '../../components/PageTransition';
import { useAuth } from '../../contexts/AuthContext';
import { ProtectedRoute } from '../../components/RouteProtector';

interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
}

export default function TasksPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAddingTask, setIsAddingTask] = useState(false);
  const [deletingTaskId, setDeletingTaskId] = useState<number | null>(null);
  const [updatingTaskId, setUpdatingTaskId] = useState<number | null>(null);

  // Load tasks on component mount
  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);

      // Get the auth token from cookies
      const cookies = document.cookie.split('; ');
      const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
      const token = authTokenRow ? authTokenRow.split('=')[1] : null;

      if (!token) {
        return; // Will be handled by ProtectedRoute
      }

      const response = await fetch('/api/tasks', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.status === 401) {
        // Token expired or invalid, will be handled by ProtectedRoute
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
        return; // Will be handled by ProtectedRoute
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
        // Token expired or invalid, will be handled by ProtectedRoute
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
        return; // Will be handled by ProtectedRoute
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
        // Token expired or invalid, will be handled by ProtectedRoute
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
        return; // Will be handled by ProtectedRoute
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
        // Token expired or invalid, will be handled by ProtectedRoute
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
              My Tasks
            </h1>
            <p className="text-gray-400 mt-2">Manage your daily tasks and boost productivity</p>
          </motion.div>

          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 rounded-lg bg-red-500/20 p-4 border border-red-500/30"
            >
              <div className="text-sm text-red-300">{error}</div>
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
            className="mt-10"
          >
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
              <h2 className="text-xl sm:text-2xl font-semibold text-white">Your Tasks</h2>
              <span className="text-gray-400 text-sm sm:text-base">
                {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
              </span>
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
                  <div className="text-gray-400 mb-4">No tasks yet</div>
                  <p className="text-gray-500">Add your first task to get started</p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4 max-h-[50vh] overflow-y-auto pr-2 custom-scrollbar">
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
      </PageTransition>
    </ProtectedRoute>
  );
}