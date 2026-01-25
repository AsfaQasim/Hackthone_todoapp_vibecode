import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';

interface ButtonProps extends HTMLMotionProps<'button'> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({
    variant = 'primary',
    size = 'md',
    isLoading = false,
    children,
    className = '',
    disabled,
    whileHover,
    whileTap,
    ...props
  }, ref) => {
    const baseClasses = 'inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-cyan-500 disabled:pointer-events-none';
    
    const variantClasses = {
      primary: 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white hover:from-cyan-700 hover:to-blue-700 focus-visible:ring-offset-gray-900',
      secondary: 'bg-gray-800 text-gray-100 hover:bg-gray-700 focus-visible:ring-offset-gray-900',
      ghost: 'text-gray-300 hover:bg-gray-800/50 focus-visible:ring-offset-gray-900',
      destructive: 'bg-red-900/30 text-red-400 hover:bg-red-900/50 focus-visible:ring-offset-gray-900 border border-red-900/50',
    };
    
    const sizeClasses = {
      sm: 'h-9 px-3 text-sm',
      md: 'h-10 px-4 py-2',
      lg: 'h-12 px-6 text-lg',
    };
    
    const disabledClass = disabled || isLoading ? 'opacity-50 cursor-not-allowed' : '';
    
    const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${disabledClass} ${className}`;
    
    return (
      <motion.button
        ref={ref}
        className={classes}
        disabled={disabled || isLoading}
        whileHover={whileHover !== undefined ? whileHover : (!disabled && !isLoading ? { scale: 1.03 } : {})}
        whileTap={whileTap !== undefined ? whileTap : (!disabled && !isLoading ? { scale: 0.98 } : {})}
        {...props}
      >
        {isLoading ? (
          <span className="flex items-center">
            <svg
              className="animate-spin -ml-1 mr-2 h-4 w-4 text-current"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Loading...
          </span>
        ) : (
          children
        )}
      </motion.button>
    );
  }
);

Button.displayName = 'Button';

export default Button;