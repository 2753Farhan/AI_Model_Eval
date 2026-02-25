// app/models/compare/page.tsx
'use client';

import { useState } from 'react';
import { useModels } from '@/lib/hooks/useModels';
import { Card } from '@/components/common/Card';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ComparisonTable } from '@/components/models/ComparisonTable';

export default function CompareModelsPage() {
  const { models, loading, compareModels } = useModels();
  const [selectedModels, setSelectedModels] = useState<string[]>([]);
  const [comparisonData, setComparisonData] = useState<any[]>([]);
  const [comparing, setComparing] = useState(false);

  const toggleModel = (modelId: string) => {
    setSelectedModels((prev) =>
      prev.includes(modelId)
        ? prev.filter((id) => id !== modelId)
        : [...prev, modelId]
    );
  };

  const handleCompare = async () => {
    if (selectedModels.length < 2) return;
    setComparing(true);
    try {
      const data = await compareModels(selectedModels);
      setComparisonData(data);
    } finally {
      setComparing(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Compare Models</h1>

      <Card title="Select Models to Compare" className="mb-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          {models.map((model) => (
            <label
              key={model.model_id}
              className={`flex items-center p-4 border rounded-lg cursor-pointer ${
                selectedModels.includes(model.model_id)
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:bg-gray-50'
              }`}
            >
              <input
                type="checkbox"
                checked={selectedModels.includes(model.model_id)}
                onChange={() => toggleModel(model.model_id)}
                className="hidden"
              />
              <div className="flex-1">
                <p className="font-medium">{model.model_id}</p>
                <p className="text-sm text-gray-500">{model.provider}</p>
              </div>
              {selectedModels.includes(model.model_id) && (
                <span className="text-blue-600">✓</span>
              )}
            </label>
          ))}
        </div>

        <button
          onClick={handleCompare}
          disabled={selectedModels.length < 2 || comparing}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
        >
          {comparing ? 'Comparing...' : 'Compare Selected'}
        </button>
      </Card>

      {comparisonData.length > 0 && (
        <Card title="Comparison Results">
          <ComparisonTable data={comparisonData} />
        </Card>
      )}
    </div>
  );
}