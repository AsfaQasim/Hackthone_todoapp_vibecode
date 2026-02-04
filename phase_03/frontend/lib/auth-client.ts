// Custom auth client implementation that uses our API routes
// This replaces Better Auth client to avoid conflicts with our proxy routes

// Mock session object for compatibility
const mockSession = {
  data: null,
  isLoading: false,
  update: () => Promise.resolve(),
  mutate: () => Promise.resolve(),
};

// Function to get session (check for our auth token)
export const getSession = async () => {
  if (typeof window !== 'undefined') {
    const cookies = document.cookie.split('; ');
    let token = null;
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith('auth_token=')) {
        token = cookie.substring('auth_token='.length);
        break;
      }
    }

    if (token) {
      try {
        // Decode JWT to get user info
        const payload = JSON.parse(atob(token.split('.')[1]));
        return {
          data: {
            user: {
              id: payload.sub || 'unknown',
              email: payload.email || 'unknown@example.com',
              name: payload.name || payload.email?.split('@')[0] || 'User'
            },
            expiresAt: new Date(payload.exp * 1000) // Convert Unix timestamp to Date
          }
        };
      } catch (error) {
        console.error('Error decoding token:', error);
        return { data: null };
      }
    }
  }

  return { data: null };
};

// Get JWT token from cookies
export function getJwt() {
  if (typeof window !== 'undefined') {
    const cookies = document.cookie.split('; ');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith('auth_token=')) {
        const parts = cookie.split('=');
        return parts[1];
      }
    }
  }
  return null;
}

// Sign in function - uses our custom API route
export async function signIn(credentials: { email: string; password: string }, options?: { callbackURL?: string }) {
  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    const data = await response.json();

    if (response.ok) {
      return { data, error: null };
    } else {
      return { data: null, error: { message: data.error || 'Login failed' } };
    }
  } catch (error) {
    console.error("Sign in error:", error);
    return { error: { message: 'Network error occurred' }, data: null };
  }
}

// Sign up function - uses our custom API route
export async function signUp(credentials: { email: string; password: string; name?: string }) {
  try {
    // Ensure name is provided or use email prefix as fallback
    const signUpData = {
      email: credentials.email,
      password: credentials.password,
      name: credentials.name || credentials.email.split('@')[0]
    };

    const response = await fetch('/api/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(signUpData),
    });

    const data = await response.json();

    if (response.ok) {
      return { data, error: null };
    } else {
      return { data: null, error: { message: data.error || 'Signup failed' } };
    }
  } catch (error) {
    console.error("Sign up error:", error);
    return { error: { message: 'Network error occurred' }, data: null };
  }
}

// Sign out function
export async function signOut(options?: { callbackURL?: string }) {
  try {
    // Remove the auth token from cookies
    document.cookie = 'auth_token=; Max-Age=0; path=/;';

    // Redirect if callbackURL is provided
    if (options?.callbackURL) {
      window.location.href = options.callbackURL || '/login';
    } else {
      window.location.href = '/login';
    }
  } catch (error) {
    console.error("Sign out error:", error);
    // Remove the auth token from cookies as fallback
    document.cookie = 'auth_token=; Max-Age=0; path=/;';

    window.location.href = options?.callbackURL || '/login';
  }
}

// Define a useSession-like function for compatibility
export function useSession() {
  if (typeof window !== 'undefined') {
    const cookies = document.cookie.split('; ');
    let tokenExists = false;
    for (let i = 0; i < cookies.length; i++) {
      if (cookies[i].startsWith('auth_token=')) {
        tokenExists = true;
        break;
      }
    }

    if (tokenExists) {
      // In a real app, we would decode the JWT to get user info
      // For now, return a basic user object
      return {
        ...mockSession,
        data: {
          user: { id: '1', email: 'user@example.com' }, // Placeholder
          expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours from now
        }
      };
    }
  }

  return mockSession;
}

// Create a simplified authClient object for compatibility
export const authClient = {
  getSession,
  signIn: {
    email: signIn
  },
  signUp: {
    email: signUp
  },
  signOut,
  useSession,
  getJwt
};