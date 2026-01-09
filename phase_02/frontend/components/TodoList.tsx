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
    <div style={{ maxWidth: '600px', margin: '20px auto', padding: '20px' }}>
      <h2>Your Todos</h2>
      
      {error && (
        <div style={{ color: 'red', padding: '10px', backgroundColor: '#ffe6e6', borderRadius: '4px', marginBottom: '10px' }}>
          {error}
        </div>
      )}
      
      <form onSubmit={handleCreateTodo} style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '20px' }}>
        <input
          type="text"
          value={newTodo.title}
          onChange={(e) => setNewTodo({...newTodo, title: e.target.value})}
          placeholder="Todo title"
          required
          style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
        <textarea
          value={newTodo.description}
          onChange={(e) => setNewTodo({...newTodo, description: e.target.value})}
          placeholder="Todo description (optional)"
          style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc', minHeight: '60px' }}
        />
        <button 
          type="submit" 
          style={{ 
            padding: '10px', 
            backgroundColor: '#0070f3', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px', 
            cursor: 'pointer' 
          }}
        >
          Add Todo
        </button>
      </form>
      
      {loading ? (
        <div>Loading todos...</div>
      ) : todos.length === 0 ? (
        <div>No todos yet. Add one above!</div>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {todos.map(todo => (
            <li 
              key={todo.id} 
              style={{ 
                padding: '15px', 
                marginBottom: '10px', 
                border: '1px solid #ddd', 
                borderRadius: '4px',
                backgroundColor: todo.completed ? '#f0f0f0' : 'white'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h3 style={{ margin: 0, textDecoration: todo.completed ? 'line-through' : 'none' }}>
                    {todo.title}
                  </h3>
                  {todo.description && (
                    <p style={{ margin: '5px 0 0 0', color: '#666' }}>{todo.description}</p>
                  )}
                </div>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <button
                    onClick={() => handleToggleTodo(todo.id, todo.completed)}
                    style={{ 
                      padding: '5px 10px', 
                      backgroundColor: todo.completed ? '#28a745' : '#ffc107', 
                      border: 'none', 
                      borderRadius: '4px', 
                      cursor: 'pointer' 
                    }}
                  >
                    {todo.completed ? 'Undo' : 'Complete'}
                  </button>
                  <button
                    onClick={() => handleDeleteTodo(todo.id)}
                    style={{ 
                      padding: '5px 10px', 
                      backgroundColor: '#dc3545', 
                      color: 'white', 
                      border: 'none', 
                      borderRadius: '4px', 
                      cursor: 'pointer' 
                    }}
                  >
                    Delete
                  </button>
                </div>
              </div>
              <small style={{ color: '#999', display: 'block', marginTop: '5px' }}>
                Created: {new Date(todo.created_at).toLocaleString()}
              </small>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}