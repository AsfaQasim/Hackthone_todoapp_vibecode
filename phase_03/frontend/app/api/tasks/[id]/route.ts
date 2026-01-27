import { NextResponse } from 'next/server';
import jwt from 'jsonwebtoken';
import { 
  getTaskById, 
  updateTask, 
  deleteTask as deleteTaskFromDb 
} from '../../../../lib/db/tasks-model';

// Helper function to get user ID from auth token in cookies
async function getUserIdFromRequest(request: Request): Promise<number | null> {
  try {
    // Get the authorization header
    const authHeader = request.headers.get('Authorization');
    let token = null;

    if (authHeader && authHeader.startsWith('Bearer ')) {
      token = authHeader.substring(7);
    } else {
      // If no Authorization header, try to get token from cookies
      // Extract cookies from the request
      const cookiesHeader = request.headers.get('cookie');
      if (cookiesHeader) {
        // Parse the cookies to find the auth_token
        const cookies = cookiesHeader.split(';').reduce((acc, cookie) => {
          const [name, value] = cookie.trim().split('=');
          acc[name] = value;
          return acc;
        }, {} as Record<string, string>);

        token = cookies.auth_token;
      }
    }

    if (!token) {
      console.log('No auth token found in request');
      return null;
    }

    // Decode the JWT token to get user info
    // In a real app, you'd use the actual JWT secret from environment variables
    const decoded: any = jwt.verify(token, process.env.BETTER_AUTH_SECRET || process.env.JWT_SECRET || 'fallback_secret');
    return decoded.userId;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
}

export async function PUT(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    // Await the params promise to resolve
    const resolvedParams = await params;

    console.log('PUT - Received params.id:', resolvedParams?.id, 'Type:', typeof resolvedParams?.id);

    // Ensure params.id is a string before parsing
    if (!resolvedParams?.id || typeof resolvedParams?.id !== 'string') {
      console.log('PUT - Missing or invalid task ID parameter:', resolvedParams?.id);
      return NextResponse.json(
        { error: 'Missing or invalid task ID' },
        { status: 400 }
      );
    }

    // Remove any potential extra characters and parse
    const cleanedId = resolvedParams.id.toString().trim();
    const taskId = parseInt(cleanedId);

    if (isNaN(taskId)) {
      console.log('PUT - Invalid task ID after parsing:', resolvedParams.id, 'Cleaned:', cleanedId);
      return NextResponse.json(
        { error: 'Invalid task ID' },
        { status: 400 }
      );
    }

    const { title, description, completed } = await request.json();

    // Get user ID from the request
    const userId = await getUserIdFromRequest(request);
    if (!userId) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    console.log(`Attempting to update task ${taskId} for user ${userId}`);

    // Verify that the task belongs to the user
    const existingTask = await getTaskById(taskId, userId);
    if (!existingTask) {
      console.log(`Task ${taskId} not found for user ${userId}`);
      return NextResponse.json(
        { error: 'Task not found or unauthorized' },
        { status: 404 }
      );
    }

    // Update the task
    const updatedTask = await updateTask(taskId, userId, {
      title,
      description,
      completed
    });

    console.log(`Successfully updated task ${taskId} for user ${userId}`);
    return NextResponse.json(updatedTask, { status: 200 });
  } catch (error) {
    console.error('Error updating task:', error);
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
    // Await the params promise to resolve
    const resolvedParams = await params;

    console.log('Received params.id:', resolvedParams?.id, 'Type:', typeof resolvedParams?.id);

    // Ensure params.id is a string before parsing
    if (!resolvedParams?.id || typeof resolvedParams?.id !== 'string') {
      console.log('Missing or invalid task ID parameter:', resolvedParams?.id);
      return NextResponse.json(
        { error: 'Missing or invalid task ID' },
        { status: 400 }
      );
    }

    // Remove any potential extra characters and parse
    const cleanedId = resolvedParams.id.toString().trim();
    const taskId = parseInt(cleanedId);

    if (isNaN(taskId)) {
      console.log('Invalid task ID after parsing:', resolvedParams.id, 'Cleaned:', cleanedId);
      return NextResponse.json(
        { error: 'Invalid task ID' },
        { status: 400 }
      );
    }

    // Get user ID from the request
    const userId = await getUserIdFromRequest(request);
    if (!userId) {
      console.log('Unauthorized: No user ID found');
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    console.log(`Attempting to delete task ${taskId} for user ${userId}`);

    // Verify that the task belongs to the user
    const existingTask = await getTaskById(taskId, userId);
    if (!existingTask) {
      console.log(`Task ${taskId} not found for user ${userId}`);
      return NextResponse.json(
        { error: 'Task not found or unauthorized' },
        { status: 404 }
      );
    }

    // Delete the task
    const deletedRowCount = await deleteTaskFromDb(taskId, userId);
    console.log(`Deleted ${deletedRowCount} rows`);

    if (deletedRowCount === 0) {
      console.log(`Failed to delete task ${taskId} for user ${userId}`);
      return NextResponse.json(
        { error: 'Task not found or unauthorized' },
        { status: 404 }
      );
    }

    console.log(`Successfully deleted task ${taskId} for user ${userId}`);
    return NextResponse.json(
      { message: 'Task deleted successfully' },
      { status: 200 }
    );
  } catch (error) {
    console.error('Error deleting task:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}