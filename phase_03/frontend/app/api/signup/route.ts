import { NextResponse } from 'next/server';
import { createUser, findUserByEmail } from '../../../lib/db/models';
import { initializeDatabase } from '../../../lib/db';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { v4 as uuidv4 } from 'uuid';

let dbInitialized = false;

export async function POST(request: Request) {
  try {
    // Initialize database if not already done
    if (!dbInitialized) {
      await initializeDatabase();
      dbInitialized = true;
    }

    const { email, password } = await request.json();

    // Basic validation
    if (!email || !password) {
      return NextResponse.json(
        { error: 'Email and password are required' },
        { status: 400 }
      );
    }

    // Normalize email to lowercase
    const normalizedEmail = email.toLowerCase();

    // Check if user already exists in frontend database
    const existingUser = await findUserByEmail(normalizedEmail);
    if (existingUser) {
      return NextResponse.json(
        { error: 'User already exists' },
        { status: 409 }
      );
    }

    // Create new user with hashed password in frontend database
    const newUser = await createUser(normalizedEmail, password);

    // Also create user in backend database
    try {
      // Generate a UUID for the backend user
      const backendUserId = uuidv4();

      // Call backend API to create user (if such endpoint exists)
      // For now, we'll just create a placeholder - in a real scenario,
      // you'd have a backend endpoint to create users
      console.log(`Would create user in backend with ID: ${backendUserId}, email: ${normalizedEmail}`);
    } catch (backendError) {
      console.error('Error creating user in backend:', backendError);
      // Don't fail the signup just because backend sync failed
    }

    // Generate JWT token
    const token = jwt.sign(
      { userId: newUser.id, email: newUser.email },
      process.env.BETTER_AUTH_SECRET || process.env.JWT_SECRET || 'fallback_secret',
      { expiresIn: '24h' }
    );

    // Don't return the password in the response
    const { password: _, ...userWithoutPassword } = newUser;

    return NextResponse.json(
      {
        message: 'User created successfully',
        user: userWithoutPassword,
        token // Include the token in the response
      },
      { status: 201 }
    );
  } catch (error: any) {
    console.error('Signup error:', error);

    // Handle unique constraint violation
    if (error.message?.includes('already exists')) {
      return NextResponse.json(
        { error: 'User with this email already exists' },
        { status: 409 }
      );
    }

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}