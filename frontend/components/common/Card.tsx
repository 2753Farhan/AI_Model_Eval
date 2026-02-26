// components/common/Card.tsx
import { ReactNode } from 'react';

interface CardProps {
  title?: string;
  children: ReactNode;
  className?: string;
  onClick?: () => void;
}

export const Card = ({ title, children, className = '', onClick }: CardProps) => {
  return (
    <div 
      className={`card ${onClick ? 'cursor-pointer hover:shadow-md transition-shadow' : ''} ${className}`}
      onClick={onClick}
    >
      {title && <h3 className="card-title">{title}</h3>}
      <div className="text-secondary">
        {children}
      </div>
    </div>
  );
};