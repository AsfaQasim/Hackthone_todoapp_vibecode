import { auth } from './auth';
import { getTokens } from './auth';

/**
 * Get the session token from Better Auth
 * @returns Promise<string | null> - The session token or null if not authenticated
 */
export async function getAuthToken(): Promise<string | null> {
  try {
    // Get the session from Better Auth
    const token = localStorage.getItem('access_token');
    return token;
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
  // Check if we're online before making the request
  if (!navigator.onLine) {
    throw new Error('No internet connection. Please check your network and try again.');
  }

  // Use credentials: 'include' to automatically send cookies with the request
  // This is the preferred way for Better Auth session handling
  const fetchOptions: RequestInit = {
    ...options,
    credentials: 'include', // This ensures cookies are sent with the request
  };

  // Add authorization header if needed (for Bearer token approach)
  const token = await getAuthToken();
  if (token) {
    fetchOptions.headers = {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
  } else {
    // If no token in header, ensure Content-Type is still set if needed
    if (!fetchOptions.headers) {
      fetchOptions.headers = {};
    }
    if (!fetchOptions.headers['Content-Type']) {
      fetchOptions.headers['Content-Type'] = 'application/json';
    }
  }

  return fetch(url, fetchOptions);
}

/**
 * Make an authenticated API request with offline support
 * @param url - The API endpoint URL
 * @param options - Fetch options
 * @returns Promise containing the response
 */
export async function authenticatedRequestOfflineCapable(url: string, options: RequestInit = {}) {
  // Check if we're online before making the request
  if (!navigator.onLine) {
    // For offline scenarios, we might want to queue the request or return cached data
    // For now, we'll throw an error but in a real app, you might implement queuing
    throw new Error('No internet connection. This action requires an active internet connection.');
  }

  // Use credentials: 'include' to automatically send cookies with the request
  // This is the preferred way for Better Auth session handling
  const fetchOptions: RequestInit = {
    ...options,
    credentials: 'include', // This ensures cookies are sent with the request
  };

  // Add authorization header if needed (for Bearer token approach)
  const token = await getAuthToken();
  if (token) {
    fetchOptions.headers = {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
  } else {
    // If no token in header, ensure Content-Type is still set if needed
    if (!fetchOptions.headers) {
      fetchOptions.headers = {};
    }
    if (!fetchOptions.headers['Content-Type']) {
      fetchOptions.headers['Content-Type'] = 'application/json';
    }
  }

  return fetch(url, fetchOptions);
}

/**
 * Refresh session if needed before making a request
 * @param url - The API endpoint URL
 * @param options - Fetch options
 * @returns Promise containing the response
 */
export async function authenticatedRequestWithRefresh(url: string, options: RequestInit = {}) {
  // Check if session needs refresh before making the request
  try {
    const needsRefresh = await import('./better-auth-client').then(mod => mod.betterAuthClient.needsRefresh());
    if (needsRefresh) {
      const refreshResult = await import('./better-auth-client').then(mod => mod.betterAuthClient.refreshSession());
      if (refreshResult.success) {
        console.log('Session was refreshed before making request');
      } else {
        console.error('Session refresh failed:', refreshResult.error);
      }
    }
  } catch (error) {
    console.error('Error checking session refresh:', error);
  }

  // Proceed with the authenticated request
  return authenticatedRequest(url, options);
}