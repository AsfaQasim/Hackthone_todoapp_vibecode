import { authClient } from './auth-client';

// Generic function to make API calls with error handling
// This function is now simplified and doesn't handle authentication directly
// Authentication should be handled in the calling component
export async function apiCall<T>(endpoint: string, options?: RequestInit): Promise<T> {
  try {
    const url = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${endpoint}`;

    const fetchOptions = {
      ...options,
      headers: {
        ...options?.headers,
        'Content-Type': 'application/json',
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