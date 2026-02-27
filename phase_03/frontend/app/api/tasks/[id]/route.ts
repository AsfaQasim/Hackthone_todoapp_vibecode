import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function PUT(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const resolvedParams = await params;
    const taskId = resolvedParams.id;

    console.log('🔄 [PUT /api/tasks/[id]] Proxying update request for task:', taskId);

    // Get the authorization header
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      console.log('❌ [PUT /api/tasks/[id]] No authorization header');
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Extract user ID from token
    const token = authHeader.replace('Bearer ', '');
    const decoded = JSON.parse(atob(token.split('.')[1]));
    const userId = decoded.sub || decoded.userId || decoded.user_id;

    console.log('👤 [PUT /api/tasks/[id]] User ID from token:', userId);

    // Get request body
    const body = await request.json();
    console.log('📦 [PUT /api/tasks/[id]] Request body:', body);

    // Forward to backend
    const backendUrl = `${BACKEND_URL}/api/${userId}/tasks/${taskId}`;
    console.log('📡 [PUT /api/tasks/[id]] Forwarding to:', backendUrl);

    const response = await fetch(backendUrl, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': authHeader,
      },
      body: JSON.stringify(body),
    });

    console.log('📥 [PUT /api/tasks/[id]] Backend response status:', response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('❌ [PUT /api/tasks/[id]] Backend error:', errorText);
      return NextResponse.json(
        { error: errorText || 'Failed to update task' },
        { status: response.status }
      );
    }

    const data = await response.json();
    console.log('✅ [PUT /api/tasks/[id]] Task updated successfully');
    return NextResponse.json(data);
  } catch (error) {
    console.error('❌ [PUT /api/tasks/[id]] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const resolvedParams = await params;
    const taskId = resolvedParams.id;

    console.log('🗑️ [DELETE /api/tasks/[id]] Proxying delete request for task:', taskId);

    // Get the authorization header
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      console.log('❌ [DELETE /api/tasks/[id]] No authorization header');
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Extract user ID from token
    const token = authHeader.replace('Bearer ', '');
    const decoded = JSON.parse(atob(token.split('.')[1]));
    const userId = decoded.sub || decoded.userId || decoded.user_id;

    console.log('👤 [DELETE /api/tasks/[id]] User ID from token:', userId);

    // Forward to backend
    const backendUrl = `${BACKEND_URL}/api/${userId}/tasks/${taskId}`;
    console.log('📡 [DELETE /api/tasks/[id]] Forwarding to:', backendUrl);

    const response = await fetch(backendUrl, {
      method: 'DELETE',
      headers: {
        'Authorization': authHeader,
      },
    });

    console.log('📥 [DELETE /api/tasks/[id]] Backend response status:', response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('❌ [DELETE /api/tasks/[id]] Backend error:', errorText);
      return NextResponse.json(
        { error: errorText || 'Failed to delete task' },
        { status: response.status }
      );
    }

    const data = await response.json();
    console.log('✅ [DELETE /api/tasks/[id]] Task deleted successfully');
    return NextResponse.json(data);
  } catch (error) {
    console.error('❌ [DELETE /api/tasks/[id]] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}