import { NextRequest, NextResponse } from 'next/server';

// Define protected routes
const protectedRoutes = ['/dashboard', '/profile', '/settings', '/tasks'];

export function middleware(request: NextRequest) {
  // Check if the route is protected
  const isProtectedRoute = protectedRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  // Temporarily disabling server-side protection since we're moving to client-side auth
  // The client-side auth guard will handle protection of these routes
  if (isProtectedRoute) {
    // Allow the request to proceed to the client-side auth guard
    // This will handle the authentication check on the client
  }

  // Allow the request to proceed
  return NextResponse.next();
}

// Apply middleware to specific paths
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
