import { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Get the authorization header or session token from cookies
    const authHeader = request.headers.get('authorization');
    const cookieHeader = request.headers.get('cookie');

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    // Forward the request to the backend
    const backendResponse = await fetch(`${API_URL}/session`, {
      method: 'GET',
      headers: {
        'authorization': authHeader || '',
        'cookie': cookieHeader || '',
      },
    });

    const responseData = await backendResponse.json();

    if (backendResponse.ok) {
      // If session retrieval successful, return the session data
      return NextResponse.json(responseData);
    } else {
      // If session retrieval failed, return the error
      return NextResponse.json(
        { error: responseData.detail || 'Session retrieval failed' },
        { status: backendResponse.status }
      );
    }
  } catch (error) {
    console.error('Session proxy error:', error);
    return NextResponse.json(
      { error: 'Unable to connect to session service' },
      { status: 500 }
    );
  }
}