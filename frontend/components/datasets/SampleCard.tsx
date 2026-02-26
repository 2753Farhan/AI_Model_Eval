// components/datasets/SampleCard.tsx
import { DatasetSample } from '@/lib/api/datasets';
import { Card } from '@/components/common/Card';

interface SampleCardProps {
  sample: DatasetSample;
  onClick?: () => void;
  isSelected?: boolean;
}

export const SampleCard = ({ sample, onClick, isSelected }: SampleCardProps) => {
  return (
    <div
      onClick={onClick}
      className={`p-4 border rounded-lg cursor-pointer transition-all ${
        isSelected
          ? 'border-blue-500 bg-blue-50 shadow-md'
          : 'border-gray-200 hover:border-blue-300 hover:shadow-sm'
      }`}
    >
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-semibold text-sm">{sample.task_id}</h3>
        <span className={`text-xs px-2 py-1 rounded ${
          sample.difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
          sample.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
          'bg-red-100 text-red-800'
        }`}>
          {sample.difficulty || 'Unknown'}
        </span>
      </div>
      
      <p className="text-xs text-gray-600 mb-2 font-mono truncate">
        {sample.entry_point}
      </p>
      
      <p className="text-xs text-gray-500 mb-2 line-clamp-2">
        {sample.prompt.substring(0, 100)}...
      </p>
      
      {sample.tags && sample.tags.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-2">
          {sample.tags.slice(0, 3).map(tag => (
            <span key={tag} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
              {tag}
            </span>
          ))}
          {sample.tags.length > 3 && (
            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
              +{sample.tags.length - 3}
            </span>
          )}
        </div>
      )}
    </div>
  );
};