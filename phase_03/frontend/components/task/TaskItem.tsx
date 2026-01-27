'use client';

import { useState } from 'react';
import { Task } from '@/types/task'; // Assuming we have a types directory
import EditTaskForm from './EditTaskForm';

interface TaskItemProps {
  task: Task;
  onUpdate: (updatedTask: Task) => void;
  onDelete: (taskId: string) => void;
}

export default function TaskItem({ task, onUpdate, onDelete } : TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleToggleCompletion = async () => {
    setLoading(true);
    try {
      // Get the auth token from cookies
      const cookies = document.cookie.split('; ');
      const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
      const token = authTokenRow ? authTokenRow.split('=')[1] : null;

      if (!token) {
        throw new Error('User not authenticated');
      }

      // Update the task completion status via API
      const response = await fetch(`/api/tasks/${task.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ completed: !task.completed }),
      });

      if (response.status === 401) {
        // Token expired or invalid, show error message
        alert('Your session has expired. Please refresh the page or log in again.');
        return;
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to update task');
      }

      const updatedTask = await response.json();
      onUpdate(updatedTask);
    } catch (error) {
      console.error('Error toggling task completion:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      setLoading(true);
      try {
        // Get the auth token from cookies
        const cookies = document.cookie.split('; ');
        const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
        const token = authTokenRow ? authTokenRow.split('=')[1] : null;

        if (!token) {
          throw new Error('User not authenticated');
        }

        const response = await fetch(`/api/tasks/${task.id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.status === 401) {
          // Token expired or invalid, show error message
          alert('Your session has expired. Please refresh the page or log in again.');
          return;
        }

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to delete task');
        }

        onDelete(task.id);
      } catch (error) {
        console.error('Error deleting task:', error);
      } finally {
        setLoading(false);
      }
    }
  };

  const handleSaveEdit = (updatedTask: Task) => {
    onUpdate(updatedTask);
    setIsEditing(false);
  };

  return (
    <div className={`p-4 mb-3 rounded-lg border ${task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'}`}>
      {isEditing ? (
        <EditTaskForm
          task={task}
          onSave={handleSaveEdit}
          onCancel={() => setIsEditing(false)}
        />
      ) : (
        <div className="flex items-start">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleCompletion}
            disabled={loading}
            className="mt-1 mr-3 h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500"
          />
          <div className="flex-1">
            <h3 className={`text-lg ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`mt-1 ${task.completed ? 'line-through text-gray-400' : 'text-gray-600'}`}>
                {task.description}
              </p>
            )}
            <p className="text-xs text-gray-500 mt-2">
              Created: {new Date(task.created_at).toLocaleString()}
            </p>
          </div>
          <div className="flex space-x-2 ml-4">
            <button
              onClick={() => setIsEditing(true)}
              disabled={loading}
              className="p-2 text-blue-600 hover:text-blue-800 disabled:opacity-50"
              title="Edit task"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
              </svg>
            </button>
            <button
              onClick={handleDelete}
              disabled={loading}
              className="p-2 text-red-600 hover:text-red-800 disabled:opacity-50"
              title="Delete task"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}