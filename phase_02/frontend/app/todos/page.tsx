'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface Todo {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export default function TodosPage() {
  const router = useRouter();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState({ title: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check if user is authenticated by checking for auth token
    const tokenExists = document.cookie
      .split('; ')
      .find(row => row.startsWith('auth_token='));

    if (!tokenExists) {
      router.push('/login'); // Redirect to login if not authenticated
    } else {
      fetchTodos();
    }
  }, [router]);

  const fetchTodos = async () => {
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
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 401) {
        // Token expired or invalid, redirect to login
        router.push('/login');
        return;
      }

      if (!response.ok) {
        throw new Error('Failed to fetch todos');
      }

      const data = await response.json();
      setTodos(data);
    } catch (err) {
      setError('Failed to fetch todos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (e: React.FormEvent) => {
    e.preventDefault();

    // Get the auth token from cookies
    const cookies = document.cookie.split('; ');
    const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
    const token = authTokenRow ? authTokenRow.split('=')[1] : null;

    if (!token) {
      router.push('/login');
      return;
    }

    try {
      const response = await fetch('/api/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(newTodo),
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

        console.error('Add request failed:', errorData);
        throw new Error(errorData.error || `Failed to add todo: ${response.status}`);
      }

      const newTask = await response.json();
      setTodos([...todos, newTask]);
      setNewTodo({ title: '', description: '' });
    } catch (err: any) {
      setError(err.message || 'Failed to add todo');
      console.error(err);
    }
  };

  const toggleTodo = async (id: string) => {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    // Get the auth token from cookies
    const cookies = document.cookie.split('; ');
    const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
    const token = authTokenRow ? authTokenRow.split('=')[1] : null;

    if (!token) {
      router.push('/login');
      return;
    }

    try {
      const response = await fetch(`/api/tasks/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ completed: !todo.completed }),
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

        console.error('Update request failed:', errorData);
        throw new Error(errorData.error || `Failed to update todo: ${response.status}`);
      }

      const updatedTodo = await response.json();
      setTodos(todos.map(t => t.id === id ? updatedTodo : t));
    } catch (err) {
      setError('Failed to update todo');
      console.error(err);
    }
  };

  const deleteTodo = async (id: string) => {
    // Get the auth token from cookies
    const cookies = document.cookie.split('; ');
    const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
    const token = authTokenRow ? authTokenRow.split('=')[1] : null;

    if (!token) {
      router.push('/login');
      return;
    }

    try {
      const response = await fetch(`/api/tasks/${id}`, {
        method: 'DELETE',
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

        console.error('Delete request failed:', errorData);
        throw new Error(errorData.error || `Failed to delete todo: ${response.status}`);
      }

      setTodos(todos.filter(t => t.id !== id));
    } catch (err: any) {
      setError(err.message || 'Failed to delete todo');
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow rounded-lg p-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">My Todos</h1>

          <form onSubmit={handleAddTodo} className="mb-8 p-4 bg-gray-50 rounded-lg">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="md:col-span-2">
                <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                  Title
                </label>
                <input
                  type="text"
                  id="title"
                  value={newTodo.title}
                  onChange={(e) => setNewTodo({...newTodo, title: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="Todo title"
                  required
                />
              </div>
              <div className="md:col-span-2">
                <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <input
                  type="text"
                  id="description"
                  value={newTodo.description}
                  onChange={(e) => setNewTodo({...newTodo, description: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="Todo description"
                />
              </div>
            </div>
            <div className="mt-4">
              <button
                type="submit"
                className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
              >
                Add Todo
              </button>
            </div>
          </form>

          {error && (
            <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          {loading ? (
            <p className="text-center py-4">Loading todos...</p>
          ) : todos.length === 0 ? (
            <p className="text-center py-4 text-gray-500">No todos yet. Add one above!</p>
          ) : (
            <ul className="divide-y divide-gray-200">
              {todos.map((todo) => (
                <li key={todo.id} className="py-4 flex items-center justify-between">
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      checked={todo.completed}
                      onChange={() => toggleTodo(todo.id)}
                      className="h-4 w-4 text-indigo-600 rounded focus:ring-indigo-500"
                    />
                    <span className={`ml-3 ${todo.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                      {todo.title}
                    </span>
                  </div>
                  <div className="flex items-center space-x-4">
                    <span className="text-sm text-gray-500">{todo.description}</span>
                    <button
                      onClick={() => deleteTodo(todo.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}