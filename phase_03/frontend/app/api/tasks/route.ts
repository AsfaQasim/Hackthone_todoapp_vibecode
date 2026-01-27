import { NextResponse } from 'next/server';
import { initializeTasksTable } from '../../../lib/db/tasks-model';
import jwt from 'jsonwebtoken';
import { createTask, getTasksByUserId } from '../../../lib/db/tasks-model';

let dbInitialized = false;

// Helper function to get user ID from auth token in cookies
async function getUserIdFromRequest(request: Request): Promise<string | null> {
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
    const JWT_SECRET = process.env.BETTER_AUTH_SECRET || process.env.JWT_SECRET;
    if (!JWT_SECRET) {
      console.error("No JWT secret found in environment variables");
      return NextResponse.json(
        { error: 'Server configuration error: missing JWT secret' },
        { status: 500 }
      );
    }

    let decoded: any;
    try {
      decoded = jwt.verify(token, JWT_SECRET);
    } catch (verifyError: any) {
      console.error('JWT verification error:', verifyError.message);
      return NextResponse.json(
        { error: 'Invalid or expired token' },
        { status: 401 }
      );
    }

    // Return the user ID as a string (UUID format)
    return decoded.userId || decoded.sub || decoded.user_id || null;
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

    // Convert the UUID string to a number for the frontend database
    // In a real implementation, you'd map UUIDs to numeric IDs or vice versa
    // For now, we'll use a simple hash to convert the UUID string to a number
    let numericUserId: number;
    try {
      // Try to parse as integer first (in case it's already a number)
      numericUserId = parseInt(userId as string);
      if (isNaN(numericUserId)) {
        // If it's not a number, hash the string to get a number
        let hash = 0;
        const str = userId as string;
        for (let i = 0; i < str.length; i++) {
          const char = str.charCodeAt(i);
          hash = ((hash << 5) - hash) + char;
          hash |= 0; // Convert to 32-bit integer
        }
        numericUserId = Math.abs(hash);
      }
    } catch (error) {
      console.error('Error converting user ID to number:', error);
      return NextResponse.json(
        { error: 'Invalid user ID format' },
        { status: 400 }
      );
    }

    // Fetch tasks for the user
    const tasks = await getTasksByUserId(numericUserId);

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

    // Convert the UUID string to a number for the frontend database
    let numericUserId: number;
    try {
      // Try to parse as integer first (in case it's already a number)
      numericUserId = parseInt(userId as string);
      if (isNaN(numericUserId)) {
        // If it's not a number, hash the string to get a number
        let hash = 0;
        const str = userId as string;
        for (let i = 0; i < str.length; i++) {
          const char = str.charCodeAt(i);
          hash = ((hash << 5) - hash) + char;
          hash |= 0; // Convert to 32-bit integer
        }
        numericUserId = Math.abs(hash);
      }
    } catch (error) {
      console.error('Error converting user ID to number:', error);
      return NextResponse.json(
        { error: 'Invalid user ID format' },
        { status: 400 }
      );
    }

    // Create task in database
    const newTask = await createTask(numericUserId, title.trim(), description);

    return NextResponse.json(newTask, { status: 201 });
  } catch (error) {
    console.error('Error creating task:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}