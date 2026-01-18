'use client';

import { signOut } from '../lib/auth-client';
import { useRouter } from 'next/navigation';

export default function LogoutButton() {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await signOut();
      router.push('/'); // Redirect to home after logout
      router.refresh(); // Refresh the page to update the UI
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <button
      onClick={handleLogout}
      className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700"
    >
      Sign Out
    </button>
  );
}