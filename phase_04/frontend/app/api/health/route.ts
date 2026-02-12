import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Use BACKEND_URL for server-side calls (Docker container-to-container)
    // Falls back to NEXT_PUBLIC_API_URL for local development
    const API_URL = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    const backendResponse = await fetch(`${API_URL}/health`, {
      method: 'GET',
    });

    const responseData = await backendResponse.json();

    return NextResponse.json(responseData, {
      status: backendResponse.status,
    });
  } catch (error) {
    console.error('Health check proxy error:', error);
    return NextResponse.json(
      { error: 'Unable to connect to backend service' },
      { status: 500 }
    );
  }
}
