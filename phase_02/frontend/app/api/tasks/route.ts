import { NextResponse } from 'next/server';
import { initializeTasksTable } from '../../../lib/db/tasks-model';
import jwt from 'jsonwebtoken';
import { createTask, getTasksByUserId } from '../../../lib/db/tasks-model';

let dbInitialized = false;

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
      const cookies = request.headers.get('cookie');
      if (cookies) {
        const authTokenMatch = cookies.match(/auth_token=([^;]+)/);
        if (authTokenMatch) {
          token = authTokenMatch[1];
        }
      }
    }

    if (!token) {
      return null;
    }

    // Decode the JWT token to get user info
    // In a real app, you'd use the actual JWT secret from environment variables
    const decoded: any = jwt.verify(token, process.env.JWT_SECRET || 'fallback_secret');
    return decoded.userId;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
}

export async function GET(request: Request) {
  try {
    // Initialize database if not already done
    if (!dbInitialized) {
      await initializeTasksTable();
      dbInitialized = true;
    }

    // Get user ID from the request
    const userId = await getUserIdFromRequest(request);
    if (!userId) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Fetch tasks for the user
    const tasks = await getTasksByUserId(userId);

    return NextResponse.json(tasks, { status: 200 });
  } catch (error) {
    console.error('Error fetching tasks:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    // Initialize database if not already done
    if (!dbInitialized) {
      await initializeTasksTable();
      dbInitialized = true;
    }

    const { title, description } = await request.json();

    // Basic validation
    if (!title || !title.trim()) {
      return NextResponse.json(
        { error: 'Title is required' },
        { status: 400 }
      );
    }

    // Get user ID from the request
    const userId = await getUserIdFromRequest(request);
    if (!userId) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Create task in database
    const newTask = await createTask(userId, title.trim(), description);

    return NextResponse.json(newTask, { status: 201 });
  } catch (error) {
    console.error('Error creating task:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}