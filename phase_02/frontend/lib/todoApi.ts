/**
 * API client for interacting with the backend Task Management API
 */
import { authenticatedRequest } from './api';

export class TodoApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }


  /**
   * Get the Better Auth token from cookies or storage
   */
  async getToken(): Promise<string | null> {
    // Get token from localStorage
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      return token;
    }
    return null;
  }

  /**
   * Get all todos for the authenticated user
   */
  async getTodos(): Promise<any[]> {
    const response = await import('./api').then(mod => mod.authenticatedRequestWithRefresh(`${this.baseUrl}/api/tasks`));

    if (!response.ok) {
      if (response.status === 0) {
        // Network error (likely offline)
        throw new Error('Unable to connect to the server. Please check your internet connection.');
      }
      throw new Error(`Failed to fetch tasks: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get a specific todo by ID
   */
  async getTodo(todoId: string): Promise<any> {
    const response = await import('./api').then(mod => mod.authenticatedRequestWithRefresh(`${this.baseUrl}/api/tasks/${todoId}`));

    if (!response.ok) {
      if (response.status === 0) {
        // Network error (likely offline)
        throw new Error('Unable to connect to the server. Please check your internet connection.');
      }
      throw new Error(`Failed to fetch task: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Create a new todo
   */
  async createTodo(todoData: { title: string; description?: string; completed?: boolean }): Promise<any> {
    // Don't send user_id from frontend - backend will extract from token
    const { title, description, completed } = todoData;
    const requestData = { title, description, completed };

    const response = await import('./api').then(mod => mod.authenticatedRequestWithRefresh(`${this.baseUrl}/api/tasks`, {
      method: 'POST',
      body: JSON.stringify(requestData),
    }));

    if (!response.ok) {
      if (response.status === 0) {
        // Network error (likely offline)
        throw new Error('Unable to connect to the server. Please check your internet connection.');
      }
      throw new Error(`Failed to create task: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Update a todo
   */
  async updateTodo(todoId: string, todoData: { title?: string; description?: string; completed?: boolean }): Promise<any> {
    const response = await import('./api').then(mod => mod.authenticatedRequestWithRefresh(`${this.baseUrl}/api/tasks/${todoId}`, {
      method: 'PUT',
      body: JSON.stringify(todoData),
    }));

    if (!response.ok) {
      if (response.status === 0) {
        // Network error (likely offline)
        throw new Error('Unable to connect to the server. Please check your internet connection.');
      }
      throw new Error(`Failed to update task: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Delete a todo
   */
  async deleteTodo(todoId: string): Promise<void> {
    const response = await import('./api').then(mod => mod.authenticatedRequestWithRefresh(`${this.baseUrl}/api/tasks/${todoId}`, {
      method: 'DELETE',
    }));

    if (!response.ok) {
      if (response.status === 0) {
        // Network error (likely offline)
        throw new Error('Unable to connect to the server. Please check your internet connection.');
      }
      throw new Error(`Failed to delete task: ${response.statusText}`);
    }
  }

  /**
   * Toggle task completion status
   */
  async toggleTaskCompletion(todoId: string): Promise<any> {
    const response = await import('./api').then(mod => mod.authenticatedRequestWithRefresh(`${this.baseUrl}/api/tasks/${todoId}/complete`, {
      method: 'PATCH',
    }));

    if (!response.ok) {
      if (response.status === 0) {
        // Network error (likely offline)
        throw new Error('Unable to connect to the server. Please check your internet connection.');
      }
      throw new Error(`Failed to toggle task completion: ${response.statusText}`);
    }

    return response.json();
  }
}

// Create a singleton instance
export const todoApiClient = new TodoApiClient();