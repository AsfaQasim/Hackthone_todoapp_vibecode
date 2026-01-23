import React from 'react';
import ThreeBackground from './ThreeBackground';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="relative min-h-screen">
      <ThreeBackground />
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
};

export default Layout;