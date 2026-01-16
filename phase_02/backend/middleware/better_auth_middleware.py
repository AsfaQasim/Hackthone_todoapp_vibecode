from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import json


class BetterAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle Better Auth session tokens
    Converts cookie-based tokens to request state for use in route handlers
    """
    async def dispatch(self, request: Request, call_next: Callable):
        # Get the Better Auth session token from cookies
        # Check for various possible cookie names that Better Auth might use
        session_token = (
            request.cookies.get("better-auth.session_token") or
            request.cookies.get("session_token") or
            request.cookies.get("authjs.session-token") or
            request.cookies.get("__Secure-better-auth.session_token") or  # Secure cookie variant
            request.cookies.get("better-auth.refresh_token")  # Refresh token as fallback
        )

        if session_token:
            # Store the token in request state so it can be accessed by route handlers
            request.state.better_auth_token = session_token

        # Process the request
        response = await call_next(request)

        # Add security headers to response
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response