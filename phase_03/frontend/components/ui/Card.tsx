// components/ui/Card.tsx

import { ReactNode } from 'react';

interface CardContentProps {
  children: ReactNode;
  className?: string; // Add this line to allow className
}

export function CardContent({ children, className = "" }: CardContentProps) {
  return (
    <div className={`p-4 ${className}`}> 
      {children}
    </div>
  );
}

// Ensure your main Card component also supports it
interface CardProps {
  children: ReactNode;
  className?: string;
}

export function Card({ children, className = "" }: CardProps) {
  return (
    <div className={`bg-gray-900 border border-gray-800 rounded-xl overflow-hidden ${className}`}>
      {children}
    </div>
  );
}