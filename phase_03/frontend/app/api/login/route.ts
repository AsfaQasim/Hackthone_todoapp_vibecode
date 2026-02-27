import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    console.log('🔐 [/api/login] Received login request');
    
    const body = await request.json();
    console.log('📝 [/api/login] Request body email:', body.email);
    
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    console.log('🌐 [/api/login] Backend API URL:', API_URL);

    console.log('📡 [/api/login] Forwarding to backend:', `${API_URL}/login`);
    
    const backendResponse = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      credentials: 'include',
    });

    console.log('📥 [/api/login] Backend response status:', backendResponse.status);
    console.log('📥 [/api/login] Backend response ok:', backendResponse.ok);

    // Read body once (can only be read once)
    const responseData = await backendResponse.json();
    console.log('📥 [/api/login] Backend response data:', responseData);

    // Create our response with the same status
    const response = NextResponse.json(responseData, {
      status: backendResponse.status,
    });

    // Forward cookies
    const setCookieHeaders = backendResponse.headers.getSetCookie?.() || 
                             backendResponse.headers.get('set-cookie');

    if (setCookieHeaders) {
      const cookiesArray = Array.isArray(setCookieHeaders) 
        ? setCookieHeaders 
        : [setCookieHeaders];

      for (const cookieStr of cookiesArray) {
        const [nameValue] = cookieStr.split(';');
        const [name, value] = nameValue.split('=').map(s => s.trim());

        if (name && value) {
          response.cookies.set(name, value, {
            path: '/',
            httpOnly: cookieStr.includes('HttpOnly'),
            secure: cookieStr.includes('Secure') || process.env.NODE_ENV === 'production',
            sameSite: cookieStr.includes('SameSite=Strict') ? 'strict' :
                     cookieStr.includes('SameSite=Lax')   ? 'lax'   : 'none',
          });
        } else {
          response.headers.append('Set-Cookie', cookieStr);
        }
      }
    }

    console.log('✅ [/api/login] Returning response');
    return response;

  } catch (error) {
    console.error('❌ [/api/login] Login proxy error:', error);
    console.error('❌ [/api/login] Error details:', error instanceof Error ? error.message : 'Unknown error');
    console.error('❌ [/api/login] Error stack:', error instanceof Error ? error.stack : 'No stack');
    
    return NextResponse.json(
      { error: 'Unable to connect to authentication service. Is the backend running?' },
      { status: 500 }
    );
  }
}