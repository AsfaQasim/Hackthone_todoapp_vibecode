import { authClient } from './auth-client';

export async function authenticatedRequest(url: string, options: RequestInit = {}) {
  // Get the session using the client-side auth instance
  const session = await authClient.getSession();

  if (!session || !session.session) {
    throw new Error('Not authenticated');
  }

  // Extract the session token - Better Auth typically stores it in session.session.token
  const token = session.session.token || session.session.id;

  const fetchOptions = {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`, // Attach the token as Bearer
      'Content-Type': 'application/json',
    },
  };

  return fetch(url, fetchOptions);
}

// Generic function to make API calls with error handling
export async function apiCall<T>(endpoint: string, options?: RequestInit): Promise<T> {
  try {
    const url = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${endpoint}`;

    if (options?.headers && Object.keys(options.headers).some(key => key.toLowerCase() === 'authorization')) {
      // If authorization header is already provided, use it directly
      return await fetch(url, options).then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      });
    } else {
      // Otherwise, use authenticated request
      const response = await authenticatedRequest(url, options);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    }
  } catch (error) {
    console.error('API call error:', error);
    throw error;
  }
}