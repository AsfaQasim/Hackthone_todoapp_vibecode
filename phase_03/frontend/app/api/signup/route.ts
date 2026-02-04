import { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Extract the signup credentials from the request
    const body = await request.json();

    // Forward the request to the backend
    const backendResponse = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const responseData = await backendResponse.json();

    if (backendResponse.ok) {
      // Create a response object
      const response = NextResponse.json(responseData);

      // Extract the token from the response
      const { access_token } = responseData;

      if (access_token) {
        // Set the token in a cookie
        response.cookies.set('auth_token', access_token, {
          httpOnly: true,
          secure: process.env.NODE_ENV === 'production',
          maxAge: 60 * 60 * 24, // 24 hours
          path: '/',
          sameSite: 'strict',
        });
      }

      return response;
    } else {
      // If signup failed, return the error
      return NextResponse.json(
        { error: responseData.detail || 'Signup failed' },
        { status: backendResponse.status }
      );
    }
  } catch (error) {
    console.error('Signup proxy error:', error);
    return NextResponse.json(
      { error: 'Unable to connect to authentication service' },
      { status: 500 }
    );
  }
}