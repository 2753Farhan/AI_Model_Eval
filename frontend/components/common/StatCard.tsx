// components/common/StatCard.tsx
interface StatCardProps {
  value: number | string;
  label: string;
  color?: 'blue' | 'green' | 'purple' | 'orange';
}

export const StatCard = ({ value, label, color = 'blue' }: StatCardProps) => {
  const colorClasses = {
    blue: 'text-blue-600',
    green: 'text-green-600',
    purple: 'text-purple-600',
    orange: 'text-orange-600',
  };

  return (
    <div className="stat-card">
      <div className={`stat-value ${colorClasses[color]}`}>{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
};