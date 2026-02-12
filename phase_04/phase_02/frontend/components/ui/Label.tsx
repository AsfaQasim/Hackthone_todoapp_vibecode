import React from 'react';

interface LabelProps {
  children: React.ReactNode;
  required?: boolean;
  className?: string;
}

const Label = ({ children, required = false, className = '' }: LabelProps) => {
  return (
    <label className={`block text-sm font-medium text-gray-300 mb-1 ${className}`}>
      {children}
      {required && <span className="text-red-500">*</span>}
    </label>
  );
};

export default Label;