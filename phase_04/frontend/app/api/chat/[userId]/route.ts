import { NextRequest } from "next/server";
import { cookies } from "next/headers";

// Helper function to decode JWT token
function decodeToken(token: string) {
  try {
    const base64Payload = token.split(".")[1];
    const payload = Buffer.from(base64Payload, "base64").toString("ascii");
    return JSON.parse(payload);
  } catch (error) {
    console.error("Error decoding token:", error);
    return null;
  }
}

export async function POST(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  const { userId } = params;
  const body = await request.json();

  // Get token from cookies (our custom auth system)
  const cookieStore = cookies();
  const authToken = cookieStore.get("auth_token")?.value;

  if (!authToken) {
    console.log("No auth token found in cookies");
    return new Response(JSON.stringify({ error: "Authentication required" }), {
      status: 401,
    });
  }

  // Decode the token to get user info
  const decodedToken = decodeToken(authToken);

  if (!decodedToken) {
    console.log("Could not decode auth token");
    return new Response(JSON.stringify({ error: "Invalid authentication token" }), {
      status: 401,
    });
  }

  // Get user ID from token (this is the authenticated user)
  const tokenUserId = decodedToken.sub || decodedToken.userId || decodedToken.user_id;
  
  // Log for debugging
  console.log(`Chat request: path userId=${userId}, token userId=${tokenUserId}`);
  
  // Use the token's user ID (authenticated user) instead of path parameter
  // This ensures we always use the correct authenticated user
  const authenticatedUserId = tokenUserId;

  try {
    // Use BACKEND_URL for server-side calls (Docker container-to-container)
    // Falls back to NEXT_PUBLIC_API_URL for local development
    const API_URL = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    // Forward the request to the backend using the authenticated user ID
    const backendResponse = await fetch(
      `${API_URL}/api/${authenticatedUserId}/chat`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authToken}`, // Forward the token to backend
        },
        body: JSON.stringify(body),
      }
    );

    // Check if the response is OK before parsing JSON
    if (!backendResponse.ok) {
      // Try to parse the error response as JSON
      let errorData;
      try {
        errorData = await backendResponse.json();
      } catch (parseError) {
        // If the error response is not JSON, create a generic error
        errorData = {
          success: false,
          error: "Backend error",
          details: `HTTP ${backendResponse.status} - ${backendResponse.statusText}`
        };
      }

      return new Response(JSON.stringify(errorData), {
        status: backendResponse.status,
        headers: { "Content-Type": "application/json" },
      });
    }

    // Parse the successful response as JSON
    const data = await backendResponse.json();

    return new Response(JSON.stringify(data), {
      status: backendResponse.status,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error: any) {
    console.error("Backend connection failed:", error);
    return new Response(
      JSON.stringify({
        success: false,
        error: "Backend connection failed",
        details: error.message,
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
}
