'use client';

import React from 'react';
import Label from './Label';
import ErrorMessage from './ErrorMessage';

interface TextareaProps {
  label: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
  error?: string;
  rows?: number;
  required?: boolean;
  className?: string;
}

const Textarea = ({
  label,
  value,
  onChange,
  placeholder,
  error,
  rows = 3,
  required = false,
  className = ''
}: TextareaProps) => {
  return (
    <div className="w-full">
      <Label required={required}>
        {label}
      </Label>
      <textarea
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        rows={rows}
        className={`w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all text-white placeholder-gray-500 ${
          error ? 'border-red-500 focus:ring-red-500' : ''
        } ${className}`}
      />
      {error && <ErrorMessage>{error}</ErrorMessage>}
    </div>
  );
};

export default Textarea;