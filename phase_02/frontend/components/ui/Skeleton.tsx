import React from 'react';

interface SkeletonProps {
  className?: string;
  count?: number;
}

const Skeleton = ({ className = '', count = 1 }: SkeletonProps) => {
  const skeletons = Array.from({ length: count }, (_, index) => (
    <div 
      key={index}
      className={`animate-pulse bg-gray-800/50 rounded-md ${className}`}
    />
  ));

  return <>{skeletons}</>;
};

export default Skeleton;