import { authClient } from './auth-client';

// Generic function to make API calls with automatic token injection
export async function apiCall<T>(endpoint: string, options?: RequestInit): Promise<T> {
  try {
    const url = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${endpoint}`;

    // Get the current session to retrieve the token
    const session = await authClient.getSession();
    const token = session?.session?.token;

    const fetchOptions = {
      ...options,
      headers: {
        ...options?.headers,
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
    };

    const response = await fetch(url, fetchOptions);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API call error:', error);
    throw error;
  }
}