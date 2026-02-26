// app/datasets/[id]/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { datasetsApi } from '@/lib/api/datasets';
import { Card } from '@/components/common/Card';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';

export default function DatasetDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const [dataset, setDataset] = useState<any>(null);
  const [samples, setSamples] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [searching, setSearching] = useState(false);
  const [pagination, setPagination] = useState({
    limit: 20,
    offset: 0,
    total: 0
  });

  useEffect(() => {
    loadDatasetInfo();
    loadSamples();
    loadStatistics();
  }, [id]);

  const loadDatasetInfo = async () => {
    try {
      const data = await datasetsApi.getInfo(id as string);
      setDataset(data);
    } catch (err) {
      setError('Failed to load dataset info');
    }
  };

  const loadSamples = async (offset = 0) => {
    setLoading(true);
    try {
      const data = await datasetsApi.getSamples(id as string, pagination.limit, offset);
      setSamples(data.samples);
      setPagination(prev => ({ ...prev, total: data.total, offset: data.offset }));
    } catch (err) {
      setError('Failed to load samples');
    } finally {
      setLoading(false);
    }
  };

  const loadStatistics = async () => {
    try {
      const data = await datasetsApi.getStatistics(id as string);
      setStats(data);
    } catch (err) {
      console.error('Failed to load statistics:', err);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadSamples(0);
      return;
    }

    setSearching(true);
    try {
      const results = await datasetsApi.search(id as string, searchQuery);
      setSearchResults(results.results);
    } catch (err) {
      setError('Search failed');
    } finally {
      setSearching(false);
    }
  };

  const handleNextPage = () => {
    const newOffset = pagination.offset + pagination.limit;
    if (newOffset < pagination.total) {
      loadSamples(newOffset);
    }
  };

  const handlePrevPage = () => {
    const newOffset = Math.max(0, pagination.offset - pagination.limit);
    loadSamples(newOffset);
  };

  if (loading && !dataset) return <LoadingSpinner />;
  if (error) return <div className="text-red-600 text-center py-8">{error}</div>;
  if (!dataset) return <div className="text-center py-8">Dataset not found</div>;

  const displaySamples = searchResults.length > 0 ? searchResults : samples;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">{dataset.name}</h1>
        <p className="text-gray-600 mt-1">{dataset.description}</p>
      </div>

      {/* Dataset Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <Card className="text-center">
          <p className="text-3xl font-bold text-blue-600">{dataset.total_problems}</p>
          <p className="text-sm text-gray-600">Total Problems</p>
        </Card>
        <Card className="text-center">
          <p className="text-3xl font-bold text-green-600">{dataset.total_test_cases}</p>
          <p className="text-sm text-gray-600">Test Cases</p>
        </Card>
        <Card className="text-center">
          <p className="text-3xl font-bold text-purple-600">{dataset.avg_test_cases.toFixed(1)}</p>
          <p className="text-sm text-gray-600">Avg Tests/Problem</p>
        </Card>
        <Card className="text-center">
          <p className="text-3xl font-bold text-orange-600">{dataset.year}</p>
          <p className="text-sm text-gray-600">Year</p>
        </Card>
      </div>

      {/* Difficulty Distribution */}
      {stats && (
        <Card title="Difficulty Distribution" className="mb-8">
          <div className="flex space-x-4">
            <div className="flex-1 text-center p-4 bg-green-50 rounded-lg">
              <p className="text-2xl font-bold text-green-600">{stats.difficulties.easy}</p>
              <p className="text-sm text-gray-600">Easy</p>
            </div>
            <div className="flex-1 text-center p-4 bg-yellow-50 rounded-lg">
              <p className="text-2xl font-bold text-yellow-600">{stats.difficulties.medium}</p>
              <p className="text-sm text-gray-600">Medium</p>
            </div>
            <div className="flex-1 text-center p-4 bg-red-50 rounded-lg">
              <p className="text-2xl font-bold text-red-600">{stats.difficulties.hard}</p>
              <p className="text-sm text-gray-600">Hard</p>
            </div>
          </div>
        </Card>
      )}

      {/* Search Bar */}
      <Card className="mb-6">
        <div className="flex space-x-2">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Search problems by keyword..."
            className="flex-1 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSearch}
            disabled={searching}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
          >
            {searching ? 'Searching...' : 'Search'}
          </button>
        </div>
      </Card>

      {/* Samples List */}
      <Card title={`Problems (${pagination.total} total)`}>
        {displaySamples.length === 0 ? (
          <p className="text-center text-gray-500 py-8">No samples found</p>
        ) : (
          <>
            <div className="space-y-3">
              {displaySamples.map((sample) => (
                <Link
                  key={sample.problem_id}
                  href={`/datasets/${id}/samples/${sample.problem_id}`}
                  className="block p-4 border rounded-lg hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <h3 className="font-semibold text-lg">{sample.task_id}</h3>
                        <span className={`px-2 py-1 text-xs rounded ${
                          sample.difficulty === 'easy' ? 'bg-green-100 text-green-800' :
                          sample.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {sample.difficulty}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">{sample.prompt_preview}</p>
                      <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                        <span>🔧 {sample.entry_point}</span>
                        <span>📋 {sample.test_count} tests</span>
                        {sample.has_solution && <span>✅ Has solution</span>}
                      </div>
                    </div>
                    <span className="text-blue-600">→</span>
                  </div>
                </Link>
              ))}
            </div>

            {/* Pagination */}
            {searchResults.length === 0 && (
              <div className="flex justify-between items-center mt-6 pt-4 border-t">
                <button
                  onClick={handlePrevPage}
                  disabled={pagination.offset === 0}
                  className="px-4 py-2 border rounded-md hover:bg-gray-50 disabled:opacity-50"
                >
                  Previous
                </button>
                <span className="text-sm text-gray-600">
                  Showing {pagination.offset + 1} to {Math.min(pagination.offset + pagination.limit, pagination.total)} of {pagination.total}
                </span>
                <button
                  onClick={handleNextPage}
                  disabled={pagination.offset + pagination.limit >= pagination.total}
                  className="px-4 py-2 border rounded-md hover:bg-gray-50 disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </Card>
    </div>
  );
}