// app/evaluations/new/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useModels } from '@/lib/hooks/useModels';
import { useEvaluation } from '@/lib/hooks/useEvaluation';
import { Card } from '@/components/common/Card';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';

export default function NewEvaluationPage() {
  const router = useRouter();
  const { models, loading } = useModels();
  const { startEvaluation } = useEvaluation();
  const [selectedModels, setSelectedModels] = useState<string[]>([]);
  const [config, setConfig] = useState({
    num_samples: 5,
    timeout: 30,
    strategies: ['zero_shot'],
  });
  const [isStarting, setIsStarting] = useState(false);

  const toggleModel = (modelId: string) => {
    setSelectedModels(prev =>
      prev.includes(modelId)
        ? prev.filter(id => id !== modelId)
        : [...prev, modelId]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedModels.length === 0) return;

    setIsStarting(true);
    try {
      const evalId = await startEvaluation(selectedModels, 'humaneval');
      router.push(`/evaluations/${evalId}`);
    } catch (error) {
      console.error('Failed to start evaluation:', error);
    } finally {
      setIsStarting(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-8">New Evaluation</h1>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Model Selection */}
        <Card title="Select Models">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
          {selectedModels.length === 0 && (
            <p className="text-sm text-red-600 mt-2">Please select at least one model</p>
          )}
        </Card>

        {/* Configuration */}
        <Card title="Configuration">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Samples per Task
              </label>
              <input
                type="number"
                value={config.num_samples}
                onChange={(e) =>
                  setConfig({ ...config, num_samples: parseInt(e.target.value) })
                }
                min={1}
                max={20}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Timeout (seconds)
              </label>
              <input
                type="number"
                value={config.timeout}
                onChange={(e) =>
                  setConfig({ ...config, timeout: parseInt(e.target.value) })
                }
                min={5}
                max={120}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Prompt Strategies
              </label>
              <select
                multiple
                value={config.strategies}
                onChange={(e) =>
                  setConfig({
                    ...config,
                    strategies: Array.from(
                      e.target.selectedOptions,
                      (option) => option.value
                    ),
                  })
                }
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="zero_shot">Zero-shot</option>
                <option value="few_shot">Few-shot</option>
                <option value="chain_of_thought">Chain of Thought</option>
              </select>
            </div>
          </div>
        </Card>

        {/* Actions */}
        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => router.back()}
            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={selectedModels.length === 0 || isStarting}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
          >
            {isStarting ? 'Starting...' : 'Start Evaluation'}
          </button>
        </div>
      </form>
    </div>
  );
}