// Example frontend login function using fetch
export async function loginUser(email: string, password: string) {
  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.ok) {
      // In a real app, you'd store the token here
      // localStorage.setItem('auth_token', data.token);
      
      // Set a cookie for the auth token (this would be done server-side in a real app)
      document.cookie = `auth_token=${data.token || 'demo_token'}; path=/;`;
      
      return { success: true, user: data.user };
    } else {
      return { success: false, error: data.error };
    }
  } catch (error) {
    console.error('Login error:', error);
    return { success: false, error: 'Network error occurred' };
  }
}

// Example frontend signup function using fetch
export async function signupUser(email: string, password: string) {
  try {
    const response = await fetch('/api/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.ok) {
      return { success: true, user: data.user };
    } else {
      return { success: false, error: data.error };
    }
  } catch (error) {
    console.error('Signup error:', error);
    return { success: false, error: 'Network error occurred' };
  }
}

// Example function to check if user is authenticated
export function isAuthenticated() {
  // In a real app, you'd validate the token
  // For this demo, we'll just check if a token exists in localStorage or cookies
  const token = document.cookie
    .split('; ')
    .find(row => row.startsWith('auth_token='))
    ?.split('=')[1];
  
  return !!token;
}

// Example function to logout user
export function logoutUser() {
  // In a real app, you'd invalidate the token on the server
  // For this demo, we'll just remove the token from localStorage and cookies
  document.cookie = 'auth_token=; Max-Age=0; path=/;';
  // localStorage.removeItem('auth_token');
}