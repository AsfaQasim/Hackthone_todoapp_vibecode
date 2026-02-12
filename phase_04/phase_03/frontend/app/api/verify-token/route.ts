import { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Get the authorization header
    const authHeader = request.headers.get('authorization');

    // Get all cookies and construct a cookie header that includes our auth_token
    const cookieHeader = request.headers.get('cookie');

    // Parse cookies to find our auth_token
    let authToken = null;
    if (cookieHeader) {
      const cookies = cookieHeader.split(';');
      for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'auth_token') {
          authToken = value;
          break;
        }
      }
    }

    // Construct the authorization header if we have an auth_token in cookies
    let finalAuthHeader = authHeader;
    if (!finalAuthHeader && authToken) {
      finalAuthHeader = `Bearer ${authToken}`;
    }

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    // Forward the request to the backend
    const backendResponse = await fetch(`${API_URL}/verify-token`, {
      method: 'GET',
      headers: {
        'authorization': finalAuthHeader || '',
        'cookie': cookieHeader || '', // Pass all cookies including auth_token
      },
    });

    const responseData = await backendResponse.json();

    if (backendResponse.ok) {
      // If token verification successful, return the user data
      return NextResponse.json(responseData);
    } else {
      // If token verification failed, return the error
      return NextResponse.json(
        { error: responseData.detail || 'Token verification failed' },
        { status: backendResponse.status }
      );
    }
  } catch (error) {
    console.error('Token verification proxy error:', error);
    return NextResponse.json(
      { error: 'Unable to connect to verification service' },
      { status: 500 }
    );
  }
}