


'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import ChatInterface from '../../components/ChatInterface';
import TaskForm from '../../components/TaskForm';
import TaskItem from '../../components/TaskItem';
import { Card, CardContent } from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import LoadingSpinner from '../../components/ui/LoadingSpinner';
import Skeleton from '../../components/ui/Skeleton';
import PageTransition from '../../components/PageTransition';
import { useAuth } from '../../contexts/AuthContext';
import { api } from '../../lib/api';
import { ProtectedRoute } from '../../components/RouteProtector';

interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
}

export default function DashboardPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAddingTask, setIsAddingTask] = useState(false);
  const [deletingTaskId, setDeletingTaskId] = useState<number | null>(null);
  const [updatingTaskId, setUpdatingTaskId] = useState<number | null>(null);

  const loadTasks = async () => {
    if (!user) return;
    try {
      setLoading(true);
      const data = await api.getTasks(user.id);
      setTasks(data);
    } catch (error: any) {
      console.error('Error loading tasks:', error);
      setError('Failed to load tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (title: string, description: string) => {
    if (!user) return;
    setIsAddingTask(true);
    setError(null);

    if (!title.trim()) {
      setError('Task title is required');
      setIsAddingTask(false);
      return;
    }

    try {
      const newTask = await api.createTask(user.id, { title, description });
      setTasks(prev => [newTask, ...prev]);
    } catch (error: any) {
      console.error('Error adding task:', error);
      setError('Failed to add task. Please try again.');
    } finally {
      setIsAddingTask(false);
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    if (!user) return;

    // Find the current task
    const currentTask = tasks.find(t => t.id === taskId);
    if (!currentTask) return;

    // Optimistically update
    setTasks(prevTasks => prevTasks.map(task =>
      task.id === taskId ? { ...task, completed: !task.completed } : task
    ));

    setUpdatingTaskId(taskId);

    try {
      // Assuming Toggle endpoint is just a toggle, or if we need to send state
      // api.toggleTaskCompletion handles PATCH /tasks/{id}/complete
      // But wait, my api.ts defined toggleTaskCompletion as just calling endpoint.
      // And routes/tasks.py implemented `patch /{user_id}/tasks/{task_id}/complete`.
      const updatedTask = await api.toggleTaskCompletion(user.id, taskId.toString());

      setTasks(prevTasks => prevTasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (error: any) {
      console.error('Error toggling task:', error);
      // Revert optimism
      setTasks(prevTasks => prevTasks.map(task =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      ));
      setError('Failed to update task');
    } finally {
      setUpdatingTaskId(null);
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (!user) return;
    setDeletingTaskId(taskId);

    try {
      await api.deleteTask(user.id, taskId.toString());
      setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
    } catch (error: any) {
      console.error('Error deleting task:', error);
      setError('Failed to delete task');
    } finally {
      setDeletingTaskId(null);
    }
  };

  return (
    <ProtectedRoute>
      <PageTransition>
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

                <ChatInterface userId={user?.id || ''} onTaskAdded={loadTasks} />
              </div>
            </div>
          </main>
        </div>
      </PageTransition>
    </ProtectedRoute>
  );
}