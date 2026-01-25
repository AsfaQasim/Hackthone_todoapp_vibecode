'use client';

import React from 'react';
import ThreeBackground from './ThreeBackground';
import Sidebar from './Sidebar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="relative min-h-screen flex flex-col md:flex-row">
      <ThreeBackground />
      <Sidebar />
      <main className="flex-1 pb-16 md:pb-0 md:ml-0 lg:ml-64 transition-all duration-300">
        <div className="relative z-10 min-h-screen pt-16 md:pt-0">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;