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

  // Verify that the user ID in the token matches the path parameter
  const tokenUserId = decodedToken.sub || decodedToken.userId || decodedToken.user_id;

  if (tokenUserId !== userId) {
    console.log(`User ID mismatch: token=${tokenUserId}, path=${userId}`);
    return new Response(JSON.stringify({ error: "Unauthorized access" }), {
      status: 403,
    });
  }

  try {
    // Forward the request to the backend
    const backendResponse = await fetch(
      `http://localhost:8000/api/${userId}/chat`,
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
