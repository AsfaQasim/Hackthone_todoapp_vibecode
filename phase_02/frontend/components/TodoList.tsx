


































"use client";

import { useState, useEffect } from "react";
import { todoApiClient } from "@/lib/todoApi";
import { useSession } from "@better-auth/react";

interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export default function TodoList() {
  const { session } = useSession();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState({ title: "", description: "" });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch todos when component mounts or session changes
  useEffect(() => {
    if (session) {
      fetchTodos();
    }
  }, [session]);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      setError(null);
      const fetchedTodos = await todoApiClient.getTodos();
      setTodos(fetchedTodos);
    } catch (err) {
      console.error("Error fetching todos:", err);
      setError("Failed to load todos");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const createdTodo = await todoApiClient.createTodo({
        title: newTodo.title,
        description: newTodo.description || undefined,
      });
      
      setTodos([...todos, createdTodo]);
      setNewTodo({ title: "", description: "" });
    } catch (err) {
      console.error("Error creating todo:", err);
      setError("Failed to create todo");
    }
  };

  const handleToggleTodo = async (todoId: string, completed: boolean) => {
    try {
      const updatedTodo = await todoApiClient.updateTodo(todoId, { completed: !completed });
      setTodos(todos.map(todo => 
        todo.id === todoId ? updatedTodo : todo
      ));
    } catch (err) {
      console.error("Error updating todo:", err);
      setError("Failed to update todo");
    }
  };

  const handleDeleteTodo = async (todoId: string) => {
    try {
      await todoApiClient.deleteTodo(todoId);
      setTodos(todos.filter(todo => todo.id !== todoId));
    } catch (err) {
      console.error("Error deleting todo:", err);
      setError("Failed to delete todo");
    }
  };

  if (!session) {
    return <div>Please sign in to view your todos.</div>;
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Your Todos</h2>

      {error && (
        <div className="p-3 bg-red-50 text-red-700 rounded-md mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleCreateTodo} className="flex flex-col gap-3 mb-6">
        <input
          type="text"
          value={newTodo.title}
          onChange={(e) => setNewTodo({...newTodo, title: e.target.value})}
          placeholder="Todo title"
          required
          className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <textarea
          value={newTodo.description}
          onChange={(e) => setNewTodo({...newTodo, description: e.target.value})}
          placeholder="Todo description (optional)"
          className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[60px]"
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Add Todo
        </button>
      </form>

      {loading ? (
        <div className="text-center py-4">Loading todos...</div>
      ) : todos.length === 0 ? (
        <div className="text-center py-4">No todos yet. Add one above!</div>
      ) : (
        <ul className="list-none p-0">
          {todos.map(todo => (
            <li
              key={todo.id}
              className={`p-4 mb-3 border border-gray-300 rounded-lg ${todo.completed ? 'bg-gray-100' : 'bg-white'}`}
            >
              <div className="flex justify-between items-center">
                <div>
                  <h3 className={`${todo.completed ? 'line-through' : ''} font-medium`}>
                    {todo.title}
                  </h3>
                  {todo.description && (
                    <p className="text-gray-600 mt-1">{todo.description}</p>
                  )}
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleToggleTodo(todo.id, todo.completed)}
                    className={`px-3 py-1 rounded-md ${
                      todo.completed
                        ? 'bg-green-500 hover:bg-green-600'
                        : 'bg-yellow-500 hover:bg-yellow-600'
                    } text-white`}
                  >
                    {todo.completed ? 'Undo' : 'Complete'}
                  </button>
                  <button
                    onClick={() => handleDeleteTodo(todo.id)}
                    className="px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600"
                  >
                    Delete
                  </button>
                </div>
              </div>
              <small className="text-gray-500 block mt-2">
                Created: {new Date(todo.created_at).toLocaleString()}
              </small>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}