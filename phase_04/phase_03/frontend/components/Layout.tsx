'use client';

import React from 'react';
import { usePathname } from 'next/navigation';
import ThreeBackground from './ThreeBackground';
import Sidebar from './Sidebar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const pathname = usePathname();

  // Define routes where sidebar should NOT be shown
  const noSidebarRoutes = ['/login', '/signup', '/signin'];

  // Check if current route is an auth route
  const isAuthRoute = noSidebarRoutes.some(route => pathname === route);

  return (
    <div className="relative min-h-screen flex flex-col md:flex-row">
      <ThreeBackground />
      {!isAuthRoute && <Sidebar />}
      <main className={`flex-1 transition-all duration-300 ${!isAuthRoute ? 'md:ml-0 lg:ml-64' : ''}`}>
        <div className={`relative z-10 min-h-screen ${!isAuthRoute ? 'pt-16 md:pt-0' : ''}`}>
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;