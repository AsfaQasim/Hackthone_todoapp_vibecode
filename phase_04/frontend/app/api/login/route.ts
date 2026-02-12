import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Use BACKEND_URL for server-side calls (Docker container-to-container)
    // Falls back to NEXT_PUBLIC_API_URL for local development
    const API_URL = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    const backendResponse = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      // Important: forward incoming cookies if needed (e.g. refresh token)
      credentials: 'include', // usually not needed for server→server, but harmless
    });

    // Read body once (can only be read once)
    const responseData = await backendResponse.json();

    // Create our response with the same status
    const response = NextResponse.json(responseData, {
      status: backendResponse.status,
    });

    // ────────────────────────────────────────────────
    // Critical: Forward ALL Set-Cookie headers from backend
    const setCookieHeaders = backendResponse.headers.getSetCookie?.() || 
                             backendResponse.headers.get('set-cookie');

    if (setCookieHeaders) {
      // getSetCookie() returns string[], plain 'set-cookie' may be string
      const cookiesArray = Array.isArray(setCookieHeaders) 
        ? setCookieHeaders 
        : [setCookieHeaders];

      for (const cookieStr of cookiesArray) {
        // Parse basic name=value (you can improve parsing if needed)
        const [nameValue] = cookieStr.split(';');
        const [name, value] = nameValue.split('=').map(s => s.trim());

        if (name && value) {
          response.cookies.set(name, value, {
            // You can parse other attributes (path, httpOnly, etc.) if needed
            // For now we let backend control most options
            path: '/',
            httpOnly: cookieStr.includes('HttpOnly'),
            secure: cookieStr.includes('Secure') || process.env.NODE_ENV === 'production',
            sameSite: cookieStr.includes('SameSite=Strict') ? 'strict' :
                     cookieStr.includes('SameSite=Lax')   ? 'lax'   : 'none',
            // maxAge / expires would need more parsing if you want exact match
          });
        } else {
          // Fallback: set raw string if parsing fails (less safe)
          response.headers.append('Set-Cookie', cookieStr);
        }
      }
    }

    return response;

  } catch (error) {
    console.error('Login proxy error:', error);
    return NextResponse.json(
      { error: 'Unable to connect to authentication service' },
      { status: 500 }
    );
  }
}