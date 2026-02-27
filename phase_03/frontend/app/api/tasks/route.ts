import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Helper function to get user ID from auth token
async function getUserIdFromToken(token: string): Promise<string | null> {
  try {
    // Decode JWT token (without verification for simplicity)
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.sub || payload.userId || payload.user_id || null;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
}

export async function GET(request: Request) {
  try {
    console.log('📋 [GET /api/tasks] Fetching tasks');

    // Get auth token from Authorization header or cookies
    const authHeader = request.headers.get('Authorization');
    let token = null;

    if (authHeader && authHeader.startsWith('Bearer ')) {
      token = authHeader.substring(7);
    } else {
      const cookies = request.headers.get('cookie');
      if (cookies) {
        const authTokenMatch = cookies.match(/auth_token=([^;]+)/);
        if (authTokenMatch) {
          token = authTokenMatch[1];
        }
      }
    }

    if (!token) {
      console.log('❌ [GET /api/tasks] No auth token found');
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Get user ID from token
    const userId = await getUserIdFromToken(token);
    if (!userId) {
      console.log('❌ [GET /api/tasks] Could not extract user ID from token');
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    console.log('👤 [GET /api/tasks] User ID:', userId);

    // Forward to backend
    const backendUrl = `${BACKEND_URL}/api/${userId}/tasks`;
    console.log('📡 [GET /api/tasks] Forwarding to:', backendUrl);

    const response = await fetch(backendUrl, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    console.log('📥 [GET /api/tasks] Backend response status:', response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('❌ [GET /api/tasks] Backend error:', errorText);
      return NextResponse.json(
        { error: errorText || 'Failed to fetch tasks' },
        { status: response.status }
      );
    }

    const tasks = await response.json();
    console.log('✅ [GET /api/tasks] Fetched', tasks.length, 'tasks');
    return NextResponse.json(tasks);
  } catch (error) {
    console.error('❌ [GET /api/tasks] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    console.log('➕ [POST /api/tasks] Creating task');

    // Get auth token from Authorization header or cookies
    const authHeader = request.headers.get('Authorization');
    let token = null;

    if (authHeader && authHeader.startsWith('Bearer ')) {
      token = authHeader.substring(7);
    } else {
      const cookies = request.headers.get('cookie');
      if (cookies) {
        const authTokenMatch = cookies.match(/auth_token=([^;]+)/);
        if (authTokenMatch) {
          token = authTokenMatch[1];
        }
      }
    }

    if (!token) {
      console.log('❌ [POST /api/tasks] No auth token found');
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Get user ID from token
    const userId = await getUserIdFromToken(token);
    if (!userId) {
      console.log('❌ [POST /api/tasks] Could not extract user ID from token');
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    console.log('👤 [POST /api/tasks] User ID:', userId);
    console.log('🔑 [POST /api/tasks] Token (first 20 chars):', token.substring(0, 20));

    // Get request body
    const body = await request.json();
    console.log('📦 [POST /api/tasks] Request body:', body);

    // Forward to backend
    const backendUrl = `${BACKEND_URL}/api/${userId}/tasks`;
    console.log('📡 [POST /api/tasks] Forwarding to:', backendUrl);
    console.log('📡 [POST /api/tasks] Authorization header:', `Bearer ${token.substring(0, 20)}...`);

    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(body),
    });

    console.log('📥 [POST /api/tasks] Backend response status:', response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('❌ [POST /api/tasks] Backend error:', errorText);
      return NextResponse.json(
        { error: errorText || 'Failed to create task' },
        { status: response.status }
      );
    }

    const task = await response.json();
    console.log('✅ [POST /api/tasks] Task created with ID:', task.id);
    return NextResponse.json(task, { status: 201 });
  } catch (error) {
    console.error('❌ [POST /api/tasks] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}