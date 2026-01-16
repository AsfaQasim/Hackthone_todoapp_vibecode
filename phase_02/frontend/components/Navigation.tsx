
















"use client";

import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import LogoutButton from "./LogoutButton";

export default function Navigation() {
  const { user } = useAuth();
  const router = useRouter();

  return (
    <nav className="flex justify-between items-center p-4 bg-gray-100 border-b border-gray-300">
      <div>
        <h1 className="m-0 text-gray-800">Todo App</h1>
      </div>
      <div className="flex items-center gap-4">
        {user && (
          <>
            <span className="text-gray-600">
              Welcome, {user.name || user.email}
            </span>
            <LogoutButton variant="outline" />
          </>
        )}
      </div>
    </nav>
  );
}