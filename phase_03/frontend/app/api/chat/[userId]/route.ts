// app/api/chat/[userId]/route.ts
import { NextRequest } from 'next/server';
import { cookies } from 'next/headers';

export async function POST(request: NextRequest, { params }: { params: { userId: string } }) {
  const { userId } = params;
  const body = await request.json();

  // Get the auth token from cookies
  const authCookie = cookies().get('auth_token');
  if (!authCookie) {
    return new Response(JSON.stringify({ error: 'Authentication token not found' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    // Forward the request to the backend
    const backendResponse = await fetch(`http://localhost:8000/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authCookie.value}`,
      },
      body: JSON.stringify(body),
    });

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