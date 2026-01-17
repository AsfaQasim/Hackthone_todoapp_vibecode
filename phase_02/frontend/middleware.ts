import { authMiddleware } from 'better-auth/next-js';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Define protected routes
const protectedRoutes = ['/dashboard', '/todos', '/profile', '/settings'];
const authRoutes = ['/signin', '/signup'];

export function middleware(request: NextRequest) {
  // Check if the route is protected
  const isProtectedRoute = protectedRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  // Check if the route is an auth route
  const isAuthRoute = authRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  // If it's a protected route, use Better Auth's middleware to check authentication
  if (isProtectedRoute) {
    const response = authMiddleware(request);

    // If the response is a redirect to sign-in, redirect to home instead
    if (response.redirect && response.url.includes('/sign-in')) {
      const url = request.nextUrl.clone();
      url.pathname = '/';
      return NextResponse.redirect(url);
    }

    // If user is authenticated, allow the request to continue
    return response;
  }

  // If user is authenticated and trying to access auth routes, redirect to dashboard
  if (isAuthRoute) {
    const response = authMiddleware(request);

    // Check if user is authenticated by looking at the response
    // If user is authenticated, redirect to dashboard
    if (response.headers.get('x-better-auth-user')) {
      const url = request.nextUrl.clone();
      url.pathname = '/dashboard';
      return NextResponse.redirect(url);
    }
  }

  // For non-protected routes, continue normally
  return NextResponse.next();
}

// Specify the paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};