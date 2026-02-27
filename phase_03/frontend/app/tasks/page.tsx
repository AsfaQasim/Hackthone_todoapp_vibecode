'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ListTodo, TrendingUp, CheckCircle2 } from 'lucide-react';
import TaskForm from '../../components/TaskForm';
import TaskItem from '../../components/TaskItem';
import { Card, CardContent } from '../../components/ui/Card';
import LoadingSpinner from '../../components/ui/LoadingSpinner';
import Skeleton from '../../components/ui/Skeleton';
import PageTransition from '../../components/PageTransition';
import { useAuth } from '../../contexts/AuthContext';
import { ProtectedRoute } from '../../components/RouteProtector';

interface Task {
  id: string | number;  // Support both UUID (string) and legacy number IDs
  user_id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
}

// Simple toast notification component
const Toast = ({ message, type = 'success', onClose }: { message: string; type?: 'success' | 'error'; onClose: () => void }) => (
  <motion.div
    initial={{ opacity: 0, y: -50, scale: 0.3 }}
    animate={{ opacity: 1, y: 0, scale: 1 }}
    exit={{ opacity: 0, scale: 0.5, transition: { duration: 0.2 } }}
    className={`fixed top-4 right-4 z-50 px-6 py-3 rounded-xl shadow-2xl backdrop-blur-lg ${
      type === 'success' 
        ? 'bg-green-500/90 text-white border border-green-400' 
        : 'bg-red-500/90 text-white border border-red-400'
    }`}
  >
    <div className="flex items-center gap-2">
      <span>{type === 'success' ? '✅' : '❌'}</span>
      <span className="font-medium">{message}</span>
    </div>
  </motion.div>
);

export default function TasksPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAddingTask, setIsAddingTask] = useState(false);
  const [deletingTaskId, setDeletingTaskId] = useState<string | number | null>(null);
  const [updatingTaskId, setUpdatingTaskId] = useState<string | number | null>(null);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  useEffect(() => {
    loadTasks();
  }, []);

  // Auto-hide toast after 3 seconds
  useEffect(() => {
    if (toast) {
      const timer = setTimeout(() => setToast(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [toast]);

  const showToast = (message: string, type: 'success' | 'error' = 'success') => {
    setToast({ message, type });
  };

  const loadTasks = async () => {
    try {
      setLoading(true);

      const cookies = document.cookie.split('; ');
      const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
      const token = authTokenRow ? authTokenRow.split('=')[1] : null;

      if (!token) {
        return;
      }

      const response = await fetch('/api/tasks', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.status === 401) {
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
      setTasks(data);
    } catch (error: any) {
      console.error('Error loading tasks:', error);
      setError(error.message || 'Failed to load tasks');
      showToast('Failed to load tasks', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (title: string, description: string) => {
    setIsAddingTask(true);
    setError(null);

    if (!title.trim()) {
      setError('Task title is required');
      showToast('Task title is required', 'error');
      setIsAddingTask(false);
      return;
    }

    try {
      const cookies = document.cookie.split('; ');
      const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
      const token = authTokenRow ? authTokenRow.split('=')[1] : null;

      if (!token) {
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

        console.error('Add task request failed:', errorData);
        throw new Error(errorData.error || `Failed to add task: ${response.status}`);
      }

      const newTask = await response.json();
      setTasks(prevTasks => [newTask, ...prevTasks]);
      
      showToast('Task added successfully! 🎉', 'success');
    } catch (error: any) {
      console.error('Error adding task:', error);
      setError(error.message || 'Failed to add task');
      showToast('Failed to add task', 'error');
    } finally {
      setIsAddingTask(false);
    }
  };

  const handleToggleComplete = async (taskId: string | number) => {
    try {
      const cookies = document.cookie.split('; ');
      const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
      const token = authTokenRow ? authTokenRow.split('=')[1] : null;

      if (!token) {
        return;
      }

      const currentTask = tasks.find(t => t.id === taskId);
      if (!currentTask) return;

      setTasks(prevTasks => prevTasks.map(task =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      ));

      setUpdatingTaskId(taskId);

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

        console.error('Update task request failed:', errorData);
        throw new Error(errorData.error || `Failed to update task: ${response.status}`);
      }

      const updatedTask = await response.json();
      setTasks(prevTasks => prevTasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));

      if (updatedTask.completed) {
        showToast('Task completed! 🎊', 'success');
      } else {
        showToast('Task marked as incomplete', 'success');
      }
    } catch (error: any) {
      console.error('Error toggling task completion:', error);
      setTasks(prevTasks => prevTasks.map(task =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      ));
      setError(error.message || 'Failed to update task');
      showToast('Failed to update task', 'error');
    } finally {
      setUpdatingTaskId(null);
    }
  };

  const handleDeleteTask = async (taskId: string | number) => {
    console.log('🗑️ DELETE TASK CALLED - Task ID:', taskId);
    
    if (!taskId) {
      console.error('❌ Invalid task ID provided:', taskId);
      setError('Invalid task ID');
      showToast('Invalid task ID', 'error');
      setDeletingTaskId(null);
      return;
    }

    setDeletingTaskId(taskId);
    console.log('🔄 Setting deleting state for task:', taskId);

    try {
      const cookies = document.cookie.split('; ');
      const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
      const token = authTokenRow ? authTokenRow.split('=')[1] : null;

      console.log('🔑 Auth token found:', token ? 'Yes' : 'No');

      if (!token) {
        console.log('❌ No auth token found in cookies');
        showToast('Please login again', 'error');
        setDeletingTaskId(null);
        return;
      }

      const deleteUrl = `/api/tasks/${taskId}`;
      console.log('📡 DELETE Request URL:', deleteUrl);

      const response = await fetch(deleteUrl, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      console.log('📥 DELETE Response status:', response.status);

      if (response.status === 401) {
        console.log('❌ Unauthorized - 401');
        showToast('Session expired. Please login again', 'error');
        setDeletingTaskId(null);
        return;
      }

      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
          console.log('❌ Error response data:', errorData);
        } catch (parseError) {
          const errorText = await response.text();
          console.log('❌ Error response text:', errorText);
          errorData = { error: errorText || `HTTP error! status: ${response.status}` };
        }

        console.error('❌ Delete request failed:', errorData);
        throw new Error(errorData.error || `Failed to delete task: ${response.status}`);
      }

      const result = await response.json();
      console.log('✅ DELETE Success:', result.message);

      // Remove task from UI
      setTasks(prevTasks => {
        const newTasks = prevTasks.filter(task => task.id !== taskId);
        console.log('✅ Task removed from UI. Remaining tasks:', newTasks.length);
        return newTasks;
      });
      
      showToast('Task deleted successfully! 🗑️', 'success');
    } catch (error: any) {
      console.error('❌ Error deleting task:', error);
      setError(error.message || 'Failed to delete task');
      showToast('Failed to delete task', 'error');
    } finally {
      setDeletingTaskId(null);
      console.log('✅ Delete operation completed');
    }
  };

  const completedTasks = tasks.filter(t => t.completed).length;
  const totalTasks = tasks.length;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  return (
    <ProtectedRoute>
      <PageTransition>
        {/* Toast Notification */}
        <AnimatePresence>
          {toast && (
            <Toast 
              message={toast.message} 
              type={toast.type} 
              onClose={() => setToast(null)} 
            />
          )}
        </AnimatePresence>
        
        <div className="max-w-full sm:max-w-md md:max-w-lg lg:max-w-4xl mx-auto px-4 py-6 sm:py-8">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-10 text-center"
          >
            <motion.div
              animate={{ 
                scale: [1, 1.05, 1],
              }}
              transition={{ 
                duration: 2,
                repeat: Infinity,
                repeatDelay: 3
              }}
              className="inline-block mb-4"
            >
              <ListTodo className="h-16 w-16 text-cyan-400 mx-auto" />
            </motion.div>
            
            <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent mb-3">
              My Tasks
            </h1>
            <p className="text-gray-400 text-lg">Manage your daily tasks and boost productivity</p>
          </motion.div>

          {/* Stats Cards */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="grid grid-cols-3 gap-4 mb-8"
          >
            <Card className="bg-gradient-to-br from-cyan-500/20 to-blue-500/10 border-cyan-500/30">
              <CardContent className="p-4 text-center">
                <TrendingUp className="h-6 w-6 text-cyan-400 mx-auto mb-2" />
                <div className="text-2xl font-bold text-white">{totalTasks}</div>
                <div className="text-xs text-gray-400">Total</div>
              </CardContent>
            </Card>
            
            <Card className="bg-gradient-to-br from-green-500/20 to-emerald-500/10 border-green-500/30">
              <CardContent className="p-4 text-center">
                <CheckCircle2 className="h-6 w-6 text-green-400 mx-auto mb-2" />
                <div className="text-2xl font-bold text-white">{completedTasks}</div>
                <div className="text-xs text-gray-400">Done</div>
              </CardContent>
            </Card>
            
            <Card className="bg-gradient-to-br from-purple-500/20 to-pink-500/10 border-purple-500/30">
              <CardContent className="p-4 text-center">
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  className="h-6 w-6 mx-auto mb-2"
                >
                  <div className="text-purple-400 text-2xl">%</div>
                </motion.div>
                <div className="text-2xl font-bold text-white">{completionRate}%</div>
                <div className="text-xs text-gray-400">Rate</div>
              </CardContent>
            </Card>
          </motion.div>

          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="mb-6 rounded-lg bg-red-500/20 p-4 border border-red-500/30"
            >
              <div className="text-sm text-red-300">{error}</div>
            </motion.div>
          )}

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <TaskForm onAddTask={handleAddTask} isLoading={isAddingTask} />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mt-10"
          >
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
              <h2 className="text-2xl sm:text-3xl font-bold text-white">Your Tasks</h2>
            </div>

            {loading ? (
              <div className="space-y-4 max-h-[50vh] overflow-y-auto pr-2 custom-scrollbar">
                {[...Array(3)].map((_, index) => (
                  <Skeleton key={index} className="h-24 w-full" />
                ))}
              </div>
            ) : tasks.length === 0 ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
              >
                <Card className="text-center py-16 bg-gradient-to-br from-gray-800/50 to-gray-900/50">
                  <CardContent>
                    <motion.div
                      animate={{ 
                        y: [0, -10, 0],
                      }}
                      transition={{ 
                        duration: 2,
                        repeat: Infinity,
                      }}
                    >
                      <ListTodo className="h-20 w-20 text-gray-600 mx-auto mb-4" />
                    </motion.div>
                    <div className="text-gray-400 text-xl mb-2">No tasks yet</div>
                    <p className="text-gray-500">Add your first task to get started 🚀</p>
                  </CardContent>
                </Card>
              </motion.div>
            ) : (
              <div 
                className="space-y-4 max-h-[60vh] overflow-y-auto pr-2 custom-scrollbar"
              >
                <AnimatePresence mode="popLayout">
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
                </AnimatePresence>
              </div>
            )}
          </motion.div>
        </div>
      </PageTransition>
    </ProtectedRoute>
  );
}