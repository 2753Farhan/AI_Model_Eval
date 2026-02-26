// app/datasets/page.tsx
'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Card } from '@/components/common/Card';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { datasetsApi } from '@/lib/api/datasets';

interface Dataset {
  id: string;
  name: string;
  description: string;
  problems: number;
  source?: string;
  year?: number;
  language?: string;
}

export default function DatasetsPage() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    setLoading(true);
    setError(null);
    try {
      // Get basic dataset list
      const data = await datasetsApi.list();
      
      // For each dataset, fetch detailed info
      const detailedDatasets = await Promise.all(
        data.map(async (d: any) => {
          try {
            const info = await datasetsApi.getInfo(d.id);
            return {
              id: d.id,
              name: info.name,
              description: info.description,
              problems: info.total_problems,
              source: info.source,
              year: info.year,
              language: Object.keys(info.languages || { 'python': 1 })[0]
            };
          } catch {
            return {
              id: d.id,
              name: d.name,
              description: d.description,
              problems: d.problems,
            };
          }
        })
      );
      
      setDatasets(detailedDatasets);
    } catch (err) {
      setError('Failed to load datasets');
      console.error('Error loading datasets:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-600 text-center py-8">{error}</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">📚 Available Datasets</h1>
        <p className="text-gray-600 mt-1">
          Browse and explore datasets for evaluating code generation models
        </p>
      </div>

      {/* Dataset Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {datasets.map((dataset) => (
          <Link key={dataset.id} href={`/datasets/${dataset.id}`}>
            <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">{dataset.name}</h2>
                  {dataset.year && (
                    <span className="text-sm text-gray-500">{dataset.year}</span>
                  )}
                </div>
                <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                  {dataset.problems} problems
                </span>
              </div>

              <p className="text-gray-600 mb-4 line-clamp-2">
                {dataset.description}
              </p>

              <div className="flex items-center text-sm text-gray-500 space-x-4">
                {dataset.source && (
                  <span className="flex items-center">
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 12H8m8 4H8m8-8H8" />
                    </svg>
                    {dataset.source}
                  </span>
                )}
                {dataset.language && (
                  <span className="flex items-center">
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                    </svg>
                    {dataset.language}
                  </span>
                )}
              </div>

              {/* Quick Stats Preview */}
              <div className="mt-4 grid grid-cols-3 gap-2 text-center text-xs">
                <div className="bg-green-50 p-2 rounded">
                  <span className="text-green-700 font-medium">Easy</span>
                </div>
                <div className="bg-yellow-50 p-2 rounded">
                  <span className="text-yellow-700 font-medium">Medium</span>
                </div>
                <div className="bg-red-50 p-2 rounded">
                  <span className="text-red-700 font-medium">Hard</span>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>

      {/* Additional Info Card */}
      <Card className="mt-8 bg-blue-50 border-blue-200">
        <div className="flex items-start space-x-4">
          <div className="text-3xl">💡</div>
          <div>
            <h3 className="font-semibold text-blue-900 mb-2">About These Datasets</h3>
            <p className="text-sm text-blue-800">
              Each dataset contains programming problems designed to evaluate code generation models.
              Click on any dataset to explore individual samples, view canonical solutions, and test
              your own code against the problem test cases.
            </p>
            <div className="mt-3 flex flex-wrap gap-2">
              <span className="bg-blue-200 text-blue-800 text-xs px-2 py-1 rounded">🔍 Browse samples</span>
              <span className="bg-blue-200 text-blue-800 text-xs px-2 py-1 rounded">🧪 Run tests</span>
              <span className="bg-blue-200 text-blue-800 text-xs px-2 py-1 rounded">📊 View metrics</span>
              <span className="bg-blue-200 text-blue-800 text-xs px-2 py-1 rounded">💻 Try custom code</span>
            </div>
          </div>
        </div>
      </Card>

      {/* Quick Actions */}
      <div className="mt-6 flex justify-end space-x-4">
        <button
          onClick={loadDatasets}
          className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
        >
          🔄 Refresh
        </button>
        <Link
          href="/playground"
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          🚀 Go to Playground
        </Link>
      </div>
    </div>
  );
}