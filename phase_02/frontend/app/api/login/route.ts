import { NextResponse } from 'next/server';
import { getUser } from '../../../lib/user-storage';

export async function POST(request: Request) {
  try {
    const { email, password } = await request.json();

    // Basic validation
    if (!email || !password) {
      return NextResponse.json(
        { error: 'Email and password are required' },
        { status: 400 }
      );
    }

    // Check if user exists and password matches
    const user = getUser(email);
    if (!user || user.password !== password) {
      return NextResponse.json(
        { error: 'Invalid email or password' },
        { status: 401 }
      );
    }

    // In a real app, you'd generate a JWT token here
    // For this demo, we'll just return a success message
    return NextResponse.json({
      message: 'Login successful',
      user: { email: user.email },
      // In a real app, you'd return a token here
      // token: generateToken(user)
    });
  } catch (error) {
    console.error('Login error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}