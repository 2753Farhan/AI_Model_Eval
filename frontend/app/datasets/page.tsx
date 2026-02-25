// app/datasets/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { Card } from '@/components/common/Card';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { apiClient } from '@/lib/api/client';

interface DatasetSample {
  task_id: string;
  prompt: string;
  canonical_solution: string;
  test: string;
  entry_point: string;
  difficulty?: string;
  tags?: string[];
}

export default function DatasetsPage() {
  const [samples, setSamples] = useState<DatasetSample[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedSample, setSelectedSample] = useState<DatasetSample | null>(null);
  const [filter, setFilter] = useState('');
  const [stats, setStats] = useState({
    total: 0,
    easy: 0,
    medium: 0,
    hard: 0,
  });

  useEffect(() => {
    fetchSamples();
  }, []);

  const fetchSamples = async () => {
    try {
      const data = await apiClient.get<{ samples: DatasetSample[]; total: number }>('/datasets/humaneval/samples?limit=50&offset=0');

      if (data && data.samples) {
        setSamples(data.samples);

        setStats({
          total: data.total,
          easy: data.samples.filter(s => s.difficulty === 'Easy').length,
          medium: data.samples.filter(s => s.difficulty === 'Medium').length,
          hard: data.samples.filter(s => s.difficulty === 'Hard').length,
        });
      }
    } catch (error) {
      console.error('Failed to fetch dataset samples:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredSamples = samples.filter(sample =>
    sample.task_id.toLowerCase().includes(filter.toLowerCase()) ||
    sample.entry_point.toLowerCase().includes(filter.toLowerCase())
  );

  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Dataset Samples</h1>
        <div className="flex space-x-4">
          <input
            type="text"
            placeholder="Search samples..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={fetchSamples}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* Dataset Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <Card className="text-center">
          <p className="text-3xl font-bold text-blue-600">{stats.total}</p>
          <p className="text-sm text-gray-600">Total Samples</p>
        </Card>
        <Card className="text-center">
          <p className="text-3xl font-bold text-green-600">{stats.easy}</p>
          <p className="text-sm text-gray-600">Easy</p>
        </Card>
        <Card className="text-center">
          <p className="text-3xl font-bold text-yellow-600">{stats.medium}</p>
          <p className="text-sm text-gray-600">Medium</p>
        </Card>
        <Card className="text-center">
          <p className="text-3xl font-bold text-red-600">{stats.hard}</p>
          <p className="text-sm text-gray-600">Hard</p>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Sample List */}
        <div className="lg:col-span-1 space-y-4 max-h-[800px] overflow-y-auto pr-2">
          {filteredSamples.map((sample) => (
            <div
              key={sample.task_id}
              onClick={() => setSelectedSample(sample)}
              className={`p-4 border rounded-lg cursor-pointer transition-all ${selectedSample?.task_id === sample.task_id
                  ? 'border-blue-500 bg-blue-50 shadow-md'
                  : 'border-gray-200 hover:border-blue-300 hover:shadow-sm'
                }`}
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-semibold text-sm">{sample.task_id}</h3>
                <span className={`text-xs px-2 py-1 rounded ${sample.difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
                    sample.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                  }`}>
                  {sample.difficulty}
                </span>
              </div>
              <p className="text-xs text-gray-600 mb-2 font-mono">
                {sample.entry_point}
              </p>
              <div className="flex flex-wrap gap-1">
                {sample.tags?.map(tag => (
                  <span key={tag} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Sample Details */}
        <div className="lg:col-span-2">
          {selectedSample ? (
            <Card title={`Sample: ${selectedSample.task_id}`}>
              <div className="space-y-6">
                {/* Metadata */}
                <div className="grid grid-cols-2 gap-4 pb-4 border-b">
                  <div>
                    <p className="text-sm text-gray-500">Entry Point</p>
                    <p className="font-mono text-sm">{selectedSample.entry_point}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Difficulty</p>
                    <p className={`text-sm font-medium ${selectedSample.difficulty === 'Easy' ? 'text-green-600' :
                        selectedSample.difficulty === 'Medium' ? 'text-yellow-600' :
                          'text-red-600'
                      }`}>
                      {selectedSample.difficulty}
                    </p>
                  </div>
                </div>

                {/* Prompt */}
                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-2">Prompt</h3>
                  <pre className="bg-gray-900 text-gray-100 p-4 rounded-md overflow-x-auto text-sm font-mono">
                    {selectedSample.prompt}
                  </pre>
                </div>

                {/* Canonical Solution */}
                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-2">Canonical Solution</h3>
                  <pre className="bg-gray-900 text-gray-100 p-4 rounded-md overflow-x-auto text-sm font-mono">
                    {selectedSample.canonical_solution}
                  </pre>
                </div>

                {/* Test Cases */}
                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-2">Test Cases</h3>
                  <pre className="bg-gray-900 text-green-100 p-4 rounded-md overflow-x-auto text-sm font-mono">
                    {selectedSample.test}
                  </pre>
                </div>

                {/* Action Buttons */}
                <div className="flex justify-end space-x-4 pt-4 border-t">
                  <button
                    onClick={() => {
                      // Copy to clipboard
                      navigator.clipboard.writeText(selectedSample.canonical_solution);
                    }}
                    className="px-4 py-2 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
                  >
                    Copy Solution
                  </button>
                  <button
                    onClick={() => {
                      // Use in playground
                      localStorage.setItem('playground_code', selectedSample.canonical_solution);
                      window.location.href = '/playground';
                    }}
                    className="px-4 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  >
                    Open in Playground
                  </button>
                </div>
              </div>
            </Card>
          ) : (
            <Card>
              <div className="text-center py-12 text-gray-500">
                <p className="text-lg mb-2">No sample selected</p>
                <p className="text-sm">Click on a sample from the list to view details</p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}