import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  description?: string;
}

const Card = ({ children, className = '', title, description }: CardProps) => {
  return (
    <div 
      className={`bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl shadow-xl p-6 ${className}`}
    >
      {(title || description) && (
        <div className="mb-4">
          {title && <h3 className="text-xl font-semibold text-white">{title}</h3>}
          {description && <p className="text-gray-400">{description}</p>}
        </div>
      )}
      {children}
    </div>
  );
};

interface CardHeaderProps {
  children: React.ReactNode;
}

const CardHeader = ({ children }: CardHeaderProps) => {
  return <div className="pb-4">{children}</div>;
};

interface CardTitleProps {
  children: React.ReactNode;
}

const CardTitle = ({ children }: CardTitleProps) => {
  return <h3 className="text-xl font-semibold text-white">{children}</h3>;
};

interface CardDescriptionProps {
  children: React.ReactNode;
}

const CardDescription = ({ children }: CardDescriptionProps) => {
  return <p className="text-gray-400">{children}</p>;
};

interface CardContentProps {
  children: React.ReactNode;
}

const CardContent = ({ children }: CardContentProps) => {
  return <div>{children}</div>;
};

interface CardFooterProps {
  children: React.ReactNode;
}

const CardFooter = ({ children }: CardFooterProps) => {
  return <div className="pt-4">{children}</div>;
};

export { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter };