// app/api/chat/[userId]/route.ts
import { NextRequest } from 'next/server';
import { headers } from 'next/headers';
import { auth } from '@/lib/auth';

export async function POST(request: NextRequest, { params }: { params: { userId: string } }) {
  const { userId } = params;
  const body = await request.json();

  // Get session using Better Auth
  let session;
  try {
    session = await auth.api.getSession({
      headers: await headers()
    });
  } catch (error) {
    console.error('Error getting session with Better Auth:', error);
  }

  if (!session) {
    console.error('No active session found with Better Auth');
    return new Response(JSON.stringify({ error: 'Authentication required' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Verify that the session user ID matches the requested userId
  if (session.user.id !== userId) {
    console.error(`User ID mismatch: session user ID ${session.user.id} does not match requested user ID ${userId}`);
    return new Response(JSON.stringify({ error: 'Unauthorized access' }), {
      status: 403,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Get the JWT token from Better Auth session to forward to backend
  // Better Auth stores the session token in the session object
  const authToken = session.session?.token || session.sessionToken;

  if (!authToken) {
    console.error('No authentication token found in Better Auth session');
    return new Response(JSON.stringify({ error: 'Authentication token not found' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    // Forward the request to the backend
    // The backend expects the route format: POST /api/{userId}/chat
    const backendResponse = await fetch(`http://localhost:8000/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
      },
      body: JSON.stringify(body),
    });

    // If backend returns 401, propagate it to the frontend
    if (backendResponse.status === 401) {
      return new Response(JSON.stringify({ error: 'Authentication failed' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Check if the response is JSON or plain text
    const contentType = backendResponse.headers.get('content-type');
    let data;

    if (contentType && contentType.includes('application/json')) {
      data = await backendResponse.json();
    } else {
      // If it's not JSON, it might be an error message
      const text = await backendResponse.text();
      console.error('Non-JSON response from backend:', text);

      // Try to parse as JSON if possible, otherwise return as error
      try {
        data = JSON.parse(text);
      } catch {
        // If it's not valid JSON, return as an error object
        data = {
          error: `Backend returned non-JSON response: ${text.substring(0, 200)}${text.length > 200 ? '...' : ''}`,
          raw_error: text
        };
      }
    }

    return new Response(JSON.stringify(data), {
      status: backendResponse.status,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error: any) {
    console.error('Error forwarding request to backend:', error);

    // Handle different types of errors
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      // Network error - backend might be down
      return new Response(JSON.stringify({
        error: 'Unable to connect to backend service. Please make sure the backend server is running on port 8000.'
      }), {
        status: 503, // Service unavailable
        headers: { 'Content-Type': 'application/json' },
      });
    }

    return new Response(JSON.stringify({
      error: 'Failed to connect to backend service',
      details: error.message
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}