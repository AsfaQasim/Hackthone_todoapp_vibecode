// Custom auth client that works with our JWT-based system
// This replaces the Better Auth client to avoid conflicts

// Mock session object for compatibility
const mockSession = {
  data: null,
  isLoading: false,
  update: () => Promise.resolve(),
  mutate: () => Promise.resolve(),
};

// Function to get session (check for our auth token)
export function useSession() {
  if (typeof window !== 'undefined') {
    const tokenExists = document.cookie
      .split('; ')
      .find(row => row.startsWith('auth_token='));

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

// Sign in function
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
      // Store the JWT token in a cookie
      const expirationDate = new Date();
      expirationDate.setDate(expirationDate.getDate() + 1); // 1 day from now

      document.cookie = `auth_token=${data.token}; path=/; expires=${expirationDate.toUTCString()}; SameSite=Lax`;

      // Redirect if callbackURL is provided
      if (options?.callbackURL) {
        window.location.href = options.callbackURL;
      }

      return { error: null, data };
    } else {
      return { error: { message: data.error || 'Login failed' }, data: null };
    }
  } catch (error) {
    return { error: { message: 'Network error occurred' }, data: null };
  }
}

// Sign up function
export async function signUp(credentials: { email: string; password: string }) {
  try {
    const response = await fetch('/api/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    const data = await response.json();

    if (response.ok) {
      // Store the JWT token in a cookie if returned
      if (data.token) {
        const expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate() + 1); // 1 day from now

        document.cookie = `auth_token=${data.token}; path=/; expires=${expirationDate.toUTCString()}; SameSite=Lax`;
      }

      return { error: null, data };
    } else {
      return { error: { message: data.error || 'Signup failed' }, data: null };
    }
  } catch (error) {
    return { error: { message: 'Network error occurred' }, data: null };
  }
}

// Sign out function
export async function signOut(options?: { callbackURL?: string }) {
  // Remove the auth token from cookies
  document.cookie = 'auth_token=; Max-Age=0; path=/;';

  // Redirect if callbackURL is provided
  if (options?.callbackURL) {
    window.location.href = options.callbackURL || '/login';
  } else {
    window.location.href = '/login';
  }
}

// Get JWT token
export function getJwt() {
  if (typeof window !== 'undefined') {
    const cookies = document.cookie.split('; ');
    const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
    if (authTokenRow) {
      return authTokenRow.split('=')[1];
    }
  }
  return null;
}

// Export a mock client object for compatibility
export const authClient = {
  signIn: { email: signIn },
  signUp: { email: signUp },
  signOut,
  useSession,
  getJwt,
  Provider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
};