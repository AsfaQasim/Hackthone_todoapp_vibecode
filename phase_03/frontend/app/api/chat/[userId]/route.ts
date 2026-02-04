import { NextRequest } from "next/server";
import { headers } from "next/headers";
import { auth } from "@/lib/auth";

export async function POST(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  const { userId } = params;
  const body = await request.json();

  let session;

  try {
    session = await auth.api.getSession({
      headers: headers(),
    });
  } catch (error) {
    console.error("Session error:", error);
  }

  console.log("SESSION:", session);

  if (!session) {
    return new Response(JSON.stringify({ error: "Authentication required" }), {
      status: 401,
    });
  }

  if (session.user.id !== userId) {
    return new Response(JSON.stringify({ error: "Unauthorized access" }), {
      status: 403,
    });
  }

  const authToken = session.session?.token;

  if (!authToken) {
    return new Response(
      JSON.stringify({ error: "Authentication token not found" }),
      { status: 401 }
    );
  }

  try {
    const backendResponse = await fetch(
      `http://localhost:8000/api/${userId}/chat`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authToken}`,
        },
        body: JSON.stringify(body),
      }
    );

    const data = await backendResponse.json();

    return new Response(JSON.stringify(data), {
      status: backendResponse.status,
    });
  } catch (error: any) {
    return new Response(
      JSON.stringify({
        error: "Backend connection failed",
        details: error.message,
      }),
      { status: 500 }
    );
  }
}
