import { auth } from './auth';

/**
 * Get the session token from Better Auth
 * @returns Promise<string | null> - The session token or null if not authenticated
 */
export async function getAuthToken(): Promise<string | null> {
  try {
    // Get the session from Better Auth
    const session = await auth.getSession();
    if (session?.session) {
      // Better Auth uses session tokens that can be sent as Bearer tokens
      return session.session.token;
    }
    return null;
  } catch (error) {
    console.error('Error getting auth token:', error);
    return null;
  }
}

/**
 * Make an authenticated API request to the backend
 * @param url - The API endpoint URL
 * @param options - Fetch options
 * @returns Promise containing the response
 */
export async function authenticatedRequest(url: string, options: RequestInit = {}) {
  const token = await getAuthToken();

  if (!token) {
    throw new Error('Not authenticated');
  }

  const headers = {
    ...options.headers,
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };

  return fetch(url, {
    ...options,
    headers,
  });
}