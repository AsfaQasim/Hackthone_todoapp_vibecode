import React from "react";


interface TextareaProps {
  label?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
  error?: string;
  rows?: number;
  className?: string;
  disabled?: boolean;
}

const Textarea = ({
  label,
  value,
  onChange,
  placeholder,
  error,
  rows = 3,
  className = "",
  disabled = false,
}: TextareaProps) => {
  return (
    <div className="space-y-1">
      {label && <label className="text-sm font-medium text-white">{label}</label>}
      <textarea
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        rows={rows}
        disabled={disabled}
        className={`w-full rounded-md border border-gray-600 bg-transparent p-2 text-white ${className}`}
      />
      {error && <p className="text-sm text-red-500">{error}</p>}
    </div>
  );
};

export default Textarea;
