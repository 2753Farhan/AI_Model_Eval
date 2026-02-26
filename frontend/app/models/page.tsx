// app/models/page.tsx
'use client';

import { useModels } from '@/lib/hooks/useModels';
import { Card } from '@/components/common/Card';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import Link from 'next/link';

export default function ModelsPage() {
  const { models, loading, error } = useModels();

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-600 text-center py-8">{error}</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Available Models</h1>
        <Link
          href="/models/compare"
          className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
        >
          Compare Models
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {models.map((model) => (
          <Card key={model.model_id} className="hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start mb-4">
              <h3 className="font-semibold text-lg">{model.model_id}</h3>
              <span
                className={`px-2 py-1 text-xs rounded ${
                  model.active
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                {model.active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <p className="text-sm text-gray-600 mb-2">Provider: {model.provider}</p>
            {model.config && (
              <pre className="text-xs bg-gray-50 p-2 rounded overflow-x-auto">
                {JSON.stringify(model.config, null, 2)}
              </pre>
            )}
          </Card>
        ))}
      </div>
    </div>
  );
}