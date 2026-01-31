import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import jwt from 'jsonwebtoken';

export async function GET(request: Request) {
  try {
    // Get the auth token from cookies using next/headers
    const authCookie = cookies().get('auth_token');

    if (!authCookie) {
      return NextResponse.json({ error: 'No authentication token found' }, { status: 401 });
    }

    const token = authCookie.value;
    
    // Verify the JWT token
    try {
      const decoded = jwt.verify(
        token,
        process.env.BETTER_AUTH_SECRET || process.env.JWT_SECRET || 'fallback_secret'
      ) as any;
      
      // Return user information from the token
      return NextResponse.json({
        user: {
          id: decoded.userId || decoded.sub || decoded.user_id || decoded.id || 'unknown',
          email: decoded.email || 'unknown@example.com',
          name: decoded.name || decoded.full_name,
        },
        session: {
          valid: true,
          exp: decoded.exp,
        }
      });
    } catch (verificationError) {
      console.error('Token verification failed:', verificationError);
      return NextResponse.json({ error: 'Invalid or expired token' }, { status: 401 });
    }
  } catch (error) {
    console.error('Session check error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}