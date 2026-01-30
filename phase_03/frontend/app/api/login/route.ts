import { NextResponse } from 'next/server';
import { findUserByEmail } from '../../../lib/db/models';
import { initializeDatabase } from '../../../lib/db';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

let dbInitialized = false;

export async function POST(request: Request) {
  try {
    // Initialize database if not already done
    if (!dbInitialized) {
      await initializeDatabase();
      dbInitialized = true;
    }

    const body = await request.json();
    console.log('Login request body:', body); // Debug log

    const { email, password } = body;

    // Basic validation
    if (!email || !password) {
      return NextResponse.json(
        { error: 'Email and password are required' },
        { status: 400 }
      );
    }

    // Normalize email to lowercase
    const normalizedEmail = email.toLowerCase();

    // Find user by email
    const user = await findUserByEmail(normalizedEmail);
    if (!user) {
      console.log('User not found for email:', normalizedEmail); // Debug log
      return NextResponse.json(
        { error: 'Invalid email or password' },
        { status: 401 }
      );
    }

    // Compare password with hashed password
    const isPasswordValid = await bcrypt.compare(password, user.password);
    console.log('Password comparison result:', isPasswordValid); // Debug log

    if (!isPasswordValid) {
      console.log('Invalid password for user:', normalizedEmail); // Debug log
      return NextResponse.json(
        { error: 'Invalid email or password' },
        { status: 401 }
      );
    }

    // Generate JWT token
    const token = jwt.sign(
      { userId: user.id, email: user.email },
      process.env.BETTER_AUTH_SECRET || process.env.JWT_SECRET || 'fallback_secret',
      { expiresIn: '24h' }
    );

    console.log('Generated token for user:', user.id); // Debug log

    // Create response with token in cookie
    const response = NextResponse.json({
      message: 'Login successful',
      user: { id: user.id, email: user.email },
      token, // Include the token in the response for compatibility
    });

    // Set HTTP-only cookie with the token
    response.cookies.set('auth_token', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production', // Use secure cookies in production
      maxAge: 60 * 60 * 24, // 24 hours
      sameSite: 'lax', // CSRF protection
      path: '/', // Cookie is available for the entire site
    });

    console.log('Set auth_token cookie'); // Debug log

    return response;
  } catch (error) {
    console.error('Login error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}