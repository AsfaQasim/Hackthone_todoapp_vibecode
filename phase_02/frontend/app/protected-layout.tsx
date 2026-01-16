"use client";

import { useAuth } from "@/lib/auth-context";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { ReactNode } from "react";
import LogoutButton from "../components/LogoutButton";

interface ProtectedLayoutProps {
  children: ReactNode;
}

export default function ProtectedLayout({ children }: ProtectedLayoutProps) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      // Redirect to sign in if not authenticated
      router.push('/');
    }
  }, [user, loading, router]);

  // If still loading, show loading state
  if (loading) {
    return (
      <div>
        <header style={{
          padding: '1rem 2rem',
          backgroundColor: '#f8f9fa',
          borderBottom: '1px solid #dee2e6'
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <h1 style={{ margin: 0, color: '#343a40' }}>Todo App</h1>
          </div>
        </header>
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: 'calc(100vh - 80px)',
          fontSize: '18px',
          padding: '2rem'
        }}>
          Loading...
        </div>
      </div>
    );
  }

  // If user is not authenticated after loading, show redirecting message
  if (!user) {
    return (
      <div>
        <header style={{
          padding: '1rem 2rem',
          backgroundColor: '#f8f9fa',
          borderBottom: '1px solid #dee2e6'
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <h1 style={{ margin: 0, color: '#343a40' }}>Todo App</h1>
          </div>
        </header>
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: 'calc(100vh - 80px)',
          fontSize: '18px',
          padding: '2rem'
        }}>
          Redirecting to sign in...
        </div>
      </div>
    );
  }

  // If user is authenticated, show the protected content with full header
  return (
    <div>
      <header style={{
        padding: '1rem 2rem',
        backgroundColor: '#f8f9fa',
        borderBottom: '1px solid #dee2e6'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <h1 style={{ margin: 0, color: '#343a40' }}>Todo App</h1>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '1rem'
          }}>
            <span style={{ color: '#495057' }}>
              Welcome, {user.name || user.email}
            </span>
            <LogoutButton variant="outline" />
          </div>
        </div>
      </header>
      {children}
    </div>
  );
}