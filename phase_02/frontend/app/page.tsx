"use client";

import { useSession } from "@better-auth/react";
import { useEffect } from "react";
import AuthComponent from "@/components/AuthComponent";
import TodoList from "@/components/TodoList";

export default function Home() {
  const { session, isPending } = useSession();

  useEffect(() => {
    if (session) {
      console.log("User session:", session);
    }
  }, [session]);

  if (isPending) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container">
      <h1>Todo Application</h1>
      {session ? (
        <div>
          <p>Welcome, {session.user.email}!</p>
          <p>User ID: {session.user.id}</p>
          <TodoList />
        </div>
      ) : (
        <div>
          <p>Please sign in to access your todos.</p>
          <AuthComponent />
        </div>
      )}
    </div>
  );
}