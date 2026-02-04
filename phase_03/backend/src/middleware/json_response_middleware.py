"""Middleware to ensure all responses are JSON for the AI Chatbot with MCP application."""

import json
import logging
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import traceback

logger = logging.getLogger(__name__)

class JsonResponseMiddleware(BaseHTTPMiddleware):
    """Middleware to ensure all responses are JSON."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        """Process the request and ensure response is JSON."""
        try:
            response = await call_next(request)
            
            # Check if the response is already JSON
            if response.headers.get("content-type", "").startswith("application/json"):
                return response
            
            # If not JSON, try to convert the response body to JSON
            # First, get the response body
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
                
            # Decode the response body
            try:
                body_text = response_body.decode("utf-8")
            except UnicodeDecodeError:
                # If we can't decode it, return a generic error
                return JSONResponse(
                    status_code=500,
                    content={
                        "success": False,
                        "error": "Internal server error",
                        "details": "Response body could not be processed"
                    }
                )
            
            # Check if the body looks like a traceback or error message
            if body_text.strip().startswith("Traceback") or "Error" in body_text or "Exception" in body_text:
                # This appears to be a traceback, return as JSON error
                logger.error(f"Traceback detected in response: {body_text}")
                return JSONResponse(
                    status_code=500,
                    content={
                        "success": False,
                        "error": "Internal server error",
                        "details": "An unexpected error occurred in the server"
                    }
                )
            
            # If the response is not JSON but doesn't appear to be an error, wrap it
            return JSONResponse(
                status_code=response.status_code,
                content={
                    "success": True,
                    "data": body_text,
                    "message": "Response converted to JSON"
                }
            )
            
        except Exception as e:
            logger.error(f"Error in JsonResponseMiddleware: {e}")
            logger.error(traceback.format_exc())
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "Internal server error",
                    "details": "An unexpected error occurred in the server"
                }
            )