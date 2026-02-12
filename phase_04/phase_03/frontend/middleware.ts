import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // API routes ko direct allow karo
  if (request.nextUrl.pathname.startsWith("/api")) {
    return NextResponse.next();
  }

  // Abhi auth checking middleware se mat karo
  // BetterAuth server-side session handle karega
  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico).*)",
  ],
};
