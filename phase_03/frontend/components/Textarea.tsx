import React from "react";


interface TextareaProps {
  label: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
  error?: string;
  rows?: number;
}

const Textarea = ({
  label,
  value,
  onChange,
  placeholder,
  error,
  rows = 3,
}: TextareaProps) => {
  return (
    <div className="space-y-1">
      <label className="text-sm font-medium text-white">{label}</label>
      <textarea
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        rows={rows}
        className="w-full rounded-md border border-gray-600 bg-transparent p-2 text-white"
      />
      {error && <p className="text-sm text-red-500">{error}</p>}
    </div>
  );
};

export default Textarea;
