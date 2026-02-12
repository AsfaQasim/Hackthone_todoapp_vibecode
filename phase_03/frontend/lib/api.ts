import { authClient } from "./auth-client";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

type RequestOptions = RequestInit & {
  requiresAuth?: boolean;
};

async function fetchWithAuth(url: string, options: RequestOptions = {}) {
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");

  if (options.requiresAuth !== false) {
    // Get the JWT token from auth client
    const token = authClient.getJwt();
    console.log("[API] URL:", `${API_BASE_URL}${url}`);
    console.log("[API] Token:", token);

    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    } else {
      console.warn("[API] No token found for this request!");
    }
  }

  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers,
  });

  console.log("[API] Response status:", response.status);

  if (!response.ok) {
    const errorBody = await response.text();
    console.error("[API] Error body:", errorBody);
    throw new Error(`API Error: ${response.status} - ${response.statusText}`);
  }

  if (response.status === 204) {
    return null;
  }

  const json = await response.json();
  console.log("[API] Response JSON:", json);
  return json;
}

export const api = {
  getTasks: (userId: string) => fetchWithAuth(`/${userId}/tasks`),
  createTask: (userId: string, task: { title: string; description?: string }) =>
    fetchWithAuth(`/${userId}/tasks`, { method: "POST", body: JSON.stringify(task) }),
  updateTask: (userId: string, taskId: string, task: Partial<{ title: string; description: string; status: string }>) =>
    fetchWithAuth(`/${userId}/tasks/${taskId}`, { method: "PUT", body: JSON.stringify(task) }),
  deleteTask: (userId: string, taskId: string) =>
    fetchWithAuth(`/${userId}/tasks/${taskId}`, { method: "DELETE" }),
  toggleTaskCompletion: (userId: string, taskId: string) =>
    fetchWithAuth(`/${userId}/tasks/${taskId}/complete`, { method: "PATCH" }),
};
