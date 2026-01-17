'use client';

import { useState, useEffect } from 'react';
import { useSession } from 'better-auth/react';
import { useRouter } from 'next/navigation';
import { apiCall } from '../../lib/api';

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
  const { data: session, isPending } = useSession();
  const router = useRouter();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState({ title: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isPending && !session) {
      router.push('/'); // Redirect to home if not authenticated
    } else if (session) {
      fetchTodos();
    }
  }, [session, isPending, router]);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const data = await apiCall<Todo[]>('/todos/');
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
    try {
      const response = await apiCall<Todo>('/todos/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newTodo),
      });
      
      setTodos([...todos, response]);
      setNewTodo({ title: '', description: '' });
    } catch (err) {
      setError('Failed to add todo');
      console.error(err);
    }
  };

  const toggleTodo = async (id: string) => {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    try {
      const response = await apiCall<Todo>(`/todos/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed: !todo.completed }),
      });

      setTodos(todos.map(t => t.id === id ? response : t));
    } catch (err) {
      setError('Failed to update todo');
      console.error(err);
    }
  };

  const deleteTodo = async (id: string) => {
    try {
      await apiCall(`/todos/${id}`, {
        method: 'DELETE',
      });
      
      setTodos(todos.filter(t => t.id !== id));
    } catch (err) {
      setError('Failed to delete todo');
      console.error(err);
    }
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