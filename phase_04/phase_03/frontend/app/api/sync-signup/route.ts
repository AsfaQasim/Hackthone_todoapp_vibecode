import { NextRequest, NextResponse } from 'next/server';
import { initializeDatabase } from '../../../lib/db';
import { createUser, findUserByEmail } from '../../../lib/db/models';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { v4 as uuidv4 } from 'uuid';

// This is a temporary utility to sync users between frontend and backend
// In a real application, you'd have a proper user synchronization mechanism

export async function POST(request: NextRequest) {
  try {
    const { email, password, backendUserId } = await request.json();

    // Initialize database
    await initializeDatabase();

    // Basic validation
    if (!email || !password || !backendUserId) {
      return NextResponse.json(
        { error: 'Email, password, and backendUserId are required' },
        { status: 400 }
      );
    }

    // Check if user already exists in frontend database
    const normalizedEmail = email.toLowerCase();
    const existingUser = await findUserByEmail(normalizedEmail);
    
    if (existingUser) {
      return NextResponse.json(
        { error: 'User already exists' },
        { status: 409 }
      );
    }

    // Create new user with hashed password in frontend database
    const newUser = await createUser(normalizedEmail, password);

    // Generate JWT token for frontend
    const frontendToken = jwt.sign(
      { userId: newUser.id, email: newUser.email },
      process.env.BETTER_AUTH_SECRET || process.env.JWT_SECRET || 'fallback_secret',
      { expiresIn: '24h' }
    );

    // In a real implementation, you would also create the user in the backend database
    // For now, we'll just return the necessary information for the frontend to work with the backend
    return NextResponse.json({
      message: 'User created successfully',
      user: {
        id: newUser.id,
        email: newUser.email,
        backendUserId: backendUserId  // This is the UUID that the backend recognizes
      },
      frontendToken,
      backendUserId  // This is what should be used for backend API calls
    });
  } catch (error: any) {
    console.error('Sync signup error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}