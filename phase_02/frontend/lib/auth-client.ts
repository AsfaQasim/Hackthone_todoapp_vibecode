// lib/auth-client.ts

interface User {
  id: string;
  email: string;
  name?: string;
}

interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

interface LoginRequest {
  email: string;
  password: string;
}

interface SignupRequest {
  email: string;
  password: string;
  name: string;
}

interface Task {
  id: string;
  title: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskCreate {
  title: string;
  completed?: boolean;
}

interface TaskUpdate {
  title?: string;
  completed?: boolean;
}

class AuthClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  /**
   * Sign in a user with email and password
   */
  async signIn(email: string, password: string): Promise<TokenResponse> {
    const endpoint = `${this.baseUrl}/api/auth/sign-in/email`;
    const requestBody: LoginRequest = { email, password };

    console.log('AuthClient.signIn - Request payload:', requestBody);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      console.log('AuthClient.signIn - Response status:', response.status);

      const responseBody = await response.json();
      console.log('AuthClient.signIn - Response body:', responseBody);

      if (!response.ok) {
        // Throw an error containing backend response detail if login fails
        const errorMessage = responseBody.detail || `Login failed with status ${response.status}`;
        
        // Check if it's a server error (5xx) which might indicate a database issue
        if (response.status >= 500) {
          throw new Error('Server error: Unable to connect to the authentication server. The server may be experiencing database connection issues. Please try again later.');
        }
        
        throw new Error(errorMessage);
      }

      // Store the access token in localStorage on successful login
      if (responseBody.access_token) {
        localStorage.setItem('access_token', responseBody.access_token);
      }

      return responseBody;
    } catch (error) {
      console.error('AuthClient.signIn - Network error:', error);
      
      // Handle fetch/network errors and throw readable error messages
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the authentication server. Please check your connection and try again.');
      }
      
      if (error instanceof Error) {
        throw error;
      }
      
      throw new Error('An unknown error occurred during sign in.');
    }
  }

  /**
   * Sign up a new user
   */
  async signUp(email: string, password: string, name: string): Promise<TokenResponse> {
    const endpoint = `${this.baseUrl}/api/auth/sign-up/email`;
    const requestBody: SignupRequest = { email, password, name };

    console.log('AuthClient.signUp - Request payload:', requestBody);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      console.log('AuthClient.signUp - Response status:', response.status);

      const responseBody = await response.json();
      console.log('AuthClient.signUp - Response body:', responseBody);

      if (!response.ok) {
        const errorMessage = responseBody.detail || `Signup failed with status ${response.status}`;
        
        // Check if it's a server error (5xx) which might indicate a database issue
        if (response.status >= 500) {
          throw new Error('Server error: Unable to connect to the authentication server. The server may be experiencing database connection issues. Please try again later.');
        }
        
        throw new Error(errorMessage);
      }

      // Store the access token in localStorage on successful signup
      if (responseBody.access_token) {
        localStorage.setItem('access_token', responseBody.access_token);
      }

      return responseBody;
    } catch (error) {
      console.error('AuthClient.signUp - Network error:', error);
      
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the authentication server. Please check your connection and try again.');
      }
      
      if (error instanceof Error) {
        throw error;
      }
      
      throw new Error('An unknown error occurred during sign up.');
    }
  }

  /**
   * Sign out the current user
   */
  async signOut(): Promise<void> {
    const endpoint = `${this.baseUrl}/api/auth/sign-out`;

    console.log('AuthClient.signOut - Initiating sign out');

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      console.log('AuthClient.signOut - Response status:', response.status);

      const responseBody = await response.json();
      console.log('AuthClient.signOut - Response body:', responseBody);

      // Clear the token from localStorage when signing out
      localStorage.removeItem('access_token');
    } catch (error) {
      console.error('AuthClient.signOut - Network error:', error);
      
      // Still remove the token even if the API call fails
      localStorage.removeItem('access_token');
      
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the authentication server. Token cleared locally.');
      }
      
      if (error instanceof Error) {
        throw error;
      }
      
      throw new Error('An unknown error occurred during sign out.');
    }
  }

  /**
   * Get the current user's session
   */
  async getSession(): Promise<{ data: { user: User } } | null> {
    const endpoint = `${this.baseUrl}/api/auth/get-session`;
    const token = localStorage.getItem('access_token');

    if (!token) {
      console.log('AuthClient.getSession - No token found in localStorage');
      return null;
    }

    console.log('AuthClient.getSession - Using token:', token.substring(0, 20) + '...');

    try {
      const response = await fetch(endpoint, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      console.log('AuthClient.getSession - Response status:', response.status);

      const responseBody = await response.json();
      console.log('AuthClient.getSession - Response body:', responseBody);

      if (!response.ok) {
        console.error(`AuthClient.getSession - Session check failed with status: ${response.status}`);
        
        // Clear the token from localStorage if session is invalid
        localStorage.removeItem('access_token');
        return null;
      }

      return responseBody;
    } catch (error) {
      console.error('AuthClient.getSession - Network error:', error);
      
      if (error instanceof TypeError && error.message.includes('fetch')) {
        console.error('AuthClient.getSession - Network error when checking session');
        // Don't remove the token on network errors, as it might be a temporary issue
        return null;
      }
      
      if (error instanceof Error) {
        console.error('AuthClient.getSession - Error:', error.message);
        return null;
      }
      
      return null;
    }
  }

  /**
   * Create a new task
   */
  async createTask(taskData: TaskCreate): Promise<Task> {
    const endpoint = `${this.baseUrl}/api/tasks`;
    const token = localStorage.getItem('access_token');

    if (!token) {
      throw new Error('No authentication token found. Please log in.');
    }

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Failed to create task: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('AuthClient.createTask - Error:', error);
      throw error;
    }
  }

  /**
   * Get all tasks for the current user
   */
  async getTasks(): Promise<Task[]> {
    const endpoint = `${this.baseUrl}/api/tasks`;
    const token = localStorage.getItem('access_token');

    if (!token) {
      throw new Error('No authentication token found. Please log in.');
    }

    try {
      const response = await fetch(endpoint, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Failed to get tasks: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('AuthClient.getTasks - Error:', error);
      throw error;
    }
  }

  /**
   * Update a task
   */
  async updateTask(taskId: string, taskData: TaskUpdate): Promise<Task> {
    const endpoint = `${this.baseUrl}/api/tasks/${taskId}`;
    const token = localStorage.getItem('access_token');

    if (!token) {
      throw new Error('No authentication token found. Please log in.');
    }

    try {
      const response = await fetch(endpoint, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Failed to update task: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('AuthClient.updateTask - Error:', error);
      throw error;
    }
  }

  /**
   * Delete a task
   */
  async deleteTask(taskId: string): Promise<void> {
    const endpoint = `${this.baseUrl}/api/tasks/${taskId}`;
    const token = localStorage.getItem('access_token');

    if (!token) {
      throw new Error('No authentication token found. Please log in.');
    }

    try {
      const response = await fetch(endpoint, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Failed to delete task: ${response.status}`);
      }
    } catch (error) {
      console.error('AuthClient.deleteTask - Error:', error);
      throw error;
    }
  }
}

// Export a singleton instance
export const authClient = new AuthClient();