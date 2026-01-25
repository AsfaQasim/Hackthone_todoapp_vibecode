import React from 'react';

interface ErrorMessageProps {
  children: React.ReactNode;
  className?: string;
}

const ErrorMessage = ({ children, className = '' }: ErrorMessageProps) => {
  return (
    <p className={`mt-1 text-sm text-red-400 ${className}`}>
      {children}
    </p>
  );
};

export default ErrorMessage;