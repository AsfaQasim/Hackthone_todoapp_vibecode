"use client";

import { authClient } from "@/lib/auth-client";
import LogoutButton from "./LogoutButton";

interface HeaderProps {
  title: string;
}

export default function Header({ title }: HeaderProps) {
  const { data: session } = authClient.useSession();

  return (
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
        <h1 style={{ margin: 0, color: '#343a40' }}>{title}</h1>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1rem'
        }}>
          {session && (
            <>
              <span style={{ color: '#495057' }}>
                Welcome, {session.user?.name || session.user?.email}
              </span>
              <LogoutButton variant="outline" />
            </>
          )}
        </div>
      </div>
    </header>
  );
}