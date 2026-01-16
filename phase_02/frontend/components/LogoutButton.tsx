"use client";

import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import { useState } from "react";

interface LogoutButtonProps {
  className?: string;
  variant?: 'primary' | 'secondary' | 'outline';
}

export default function LogoutButton({
  className = '',
  variant = 'primary'
}: LogoutButtonProps) {
  const router = useRouter();
  const { signOut } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const handleLogout = async () => {
    setIsLoading(true);
    try {
      await signOut();
      router.push('/auth/login');
      router.refresh();
    } catch (error) {
      console.error("Logout error:", error);
      setIsLoading(false);
    }
  };

  // Define button styles based on variant
  const getButtonStyles = () => {
    switch (variant) {
      case 'secondary':
        return {
          backgroundColor: '#6c757d',
          color: 'white',
          border: 'none',
        };
      case 'outline':
        return {
          backgroundColor: 'transparent',
          color: '#dc3545',
          border: '1px solid #dc3545',
        };
      case 'primary':
      default:
        return {
          backgroundColor: '#dc3545',
          color: 'white',
          border: 'none',
        };
    }
  };

  const buttonStyle = {
    ...getButtonStyles(),
    padding: '0.5rem 1rem',
    borderRadius: '4px',
    cursor: isLoading ? 'not-allowed' : 'pointer',
    opacity: isLoading ? 0.7 : 1,
    transition: 'opacity 0.2s',
    ...(className ? {} : { minWidth: '100px' }), // Default width if no class provided
  };

  return (
    <button
      onClick={handleLogout}
      disabled={isLoading}
      className={className}
      style={buttonStyle}
      aria-label="Logout"
    >
      {isLoading ? "Logging out..." : "Logout"}
    </button>
  );
}