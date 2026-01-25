export async function apiCall<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  // Get the auth token from cookies
  const cookies = document.cookie.split('; ');
  const authTokenRow = cookies.find(row => row.startsWith('auth_token='));
  const token = authTokenRow ? authTokenRow.split('=')[1] : null;
  
  const response = await fetch(endpoint, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
      ...(token && { 'Authorization': `Bearer ${token}` }),
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}