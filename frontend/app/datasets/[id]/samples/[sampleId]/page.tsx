// app/datasets/[id]/samples/[sampleId]/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { useDatasetSample } from '@/lib/hooks/useDatasetSample';
import { Card } from '@/components/common/Card';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
// import { CodeEditor } from '@/components/playground/CodeEditor';

export default function SampleDetailPage() {
  const { id, sampleId } = useParams();
  const {
    sample,
    loading,
    error,
    executionResult,
    metrics,
    executing,
    fetchSample,
    executeSolution,
    analyzeMetrics,
    testCustomCode,
  } = useDatasetSample(id as string);

  const [activeTab, setActiveTab] = useState<'details' | 'solution' | 'test' | 'metrics'>('details');
  const [customCode, setCustomCode] = useState('');
  const [showCustom, setShowCustom] = useState(false);

  useEffect(() => {
    if (sampleId) {
      fetchSample(sampleId as string);
    }
  }, [sampleId, fetchSample]);

  const handleExecute = async () => {
    if (showCustom && customCode) {
      await testCustomCode(sampleId as string, customCode);
    } else {
      await executeSolution(sampleId as string);
    }
  };

  const handleAnalyzeMetrics = async () => {
    await analyzeMetrics(sampleId as string);
    setActiveTab('metrics');
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-600 text-center py-8">{error}</div>;
  if (!sample) return <div className="text-center py-8">Sample not found</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">{sample.task_id}</h1>
        <p className="text-gray-600 mt-1">Entry Point: {sample.entry_point}</p>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex space-x-8">
          <button
            onClick={() => setActiveTab('details')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'details'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            📝 Details
          </button>
          <button
            onClick={() => setActiveTab('solution')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'solution'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            💡 Solution
          </button>
          <button
            onClick={() => setActiveTab('test')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'test'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            🧪 Test
          </button>
          <button
            onClick={() => setActiveTab('metrics')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'metrics'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            📊 Metrics
          </button>
        </nav>
      </div>

      {/* Details Tab */}
      {activeTab === 'details' && (
        <div className="space-y-6">
          <Card title="Problem Description">
            <pre className="whitespace-pre-wrap font-sans text-gray-700">
              {sample.prompt}
            </pre>
          </Card>

          <Card title="Test Cases">
            <div className="space-y-2">
              {sample.test_cases.map((test, index) => (
                <div key={index} className="p-3 bg-gray-50 rounded font-mono text-sm">
                  {test.assertion}
                </div>
              ))}
            </div>
          </Card>

          <div className="flex justify-end space-x-3">
            <button
              onClick={handleAnalyzeMetrics}
              className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
            >
              Analyze Metrics
            </button>
            <button
              onClick={() => setActiveTab('test')}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Test Solution →
            </button>
          </div>
        </div>
      )}

      {/* Solution Tab */}
      {activeTab === 'solution' && (
        <Card title="Canonical Solution">
          <pre className="bg-gray-900 text-gray-100 p-4 rounded-md overflow-x-auto text-sm font-mono">
            {sample.canonical_solution}
          </pre>
          <div className="mt-4 flex justify-end space-x-3">
            <button
              onClick={handleAnalyzeMetrics}
              className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
            >
              Analyze Metrics
            </button>
            <button
              onClick={() => {
                setShowCustom(false);
                setActiveTab('test');
              }}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Test Solution →
            </button>
          </div>
        </Card>
      )}

      {/* Test Tab */}
      {activeTab === 'test' && (
        <div className="space-y-6">
          <Card title="Test Configuration">
            <div className="mb-4">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={showCustom}
                  onChange={(e) => setShowCustom(e.target.checked)}
                  className="rounded"
                />
                <span>Use custom code instead of canonical solution</span>
              </label>
            </div>

            {showCustom && (
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Custom Python Code
                </label>
                <textarea
                  value={customCode}
                  onChange={(e) => setCustomCode(e.target.value)}
                  rows={10}
                  className="w-full p-4 font-mono text-sm border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="# Write your solution here..."
                />
              </div>
            )}

            <button
              onClick={handleExecute}
              disabled={executing}
              className="w-full py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
            >
              {executing ? 'Executing...' : '▶ Run Tests'}
            </button>
          </Card>

          {executionResult && (
            <Card title="Execution Results">
              <div className={`p-4 rounded-md ${
                executionResult.passed ? 'bg-green-50' : 'bg-red-50'
              }`}>
                <p className="font-semibold">
                  {executionResult.passed ? '✅ All Tests Passed' : '❌ Tests Failed'}
                </p>
                <p className="text-sm text-gray-600">
                  Execution time: {executionResult.execution_time_ms?.toFixed(2)}ms
                </p>
              </div>

              {executionResult.test_results && (
                <div className="mt-4 space-y-2">
                  {executionResult.test_results.map((test, i) => (
                    <div
                      key={i}
                      className={`p-2 rounded ${
                        test.passed ? 'bg-green-50' : 'bg-red-50'
                      }`}
                    >
                      <p className="text-sm">
                        {test.passed ? '✅' : '❌'} {test.message}
                      </p>
                    </div>
                  ))}
                </div>
              )}

              {executionResult.output && !executionResult.passed && (
                <div className="mt-4">
                  <h3 className="font-semibold mb-2">Error Output</h3>
                  <pre className="p-4 bg-gray-900 text-white rounded-md overflow-x-auto text-sm">
                    {executionResult.output}
                  </pre>
                </div>
              )}
            </Card>
          )}
        </div>
      )}

      {/* Metrics Tab */}
      {activeTab === 'metrics' && metrics && (
        <Card title="Code Metrics">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <MetricCard
              label="Lines of Code"
              value={metrics.metrics?.loc || metrics.metrics?.total_lines}
            />
            <MetricCard
              label="Functions"
              value={metrics.metrics?.function_count}
            />
            <MetricCard
              label="Complexity"
              value={metrics.metrics?.cyclomatic_complexity}
              format=".1f"
            />
            <MetricCard
              label="Maintainability"
              value={metrics.metrics?.maintainability_index}
              format=".1f"
              suffix="%"
            />
            <MetricCard
              label="Quality Grade"
              value={metrics.metrics?.quality_grade}
            />
            <MetricCard
              label="Test Pass Rate"
              value={metrics.metrics?.test_pass_rate}
              format="percent"
            />
            <MetricCard
              label="Tests Passed"
              value={`${metrics.metrics?.tests_passed || 0}/${metrics.metrics?.tests_total || 0}`}
            />
          </div>

          {metrics.test_results && (
            <div className="mt-6">
              <h3 className="font-semibold mb-3">Test Results</h3>
              <div className="space-y-2">
                {metrics.test_results.test_results?.map((test: any, i: number) => (
                  <div
                    key={i}
                    className={`p-2 rounded ${
                      test.passed ? 'bg-green-50' : 'bg-red-50'
                    }`}
                  >
                    <p className="text-sm">
                      {test.passed ? '✅' : '❌'} {test.message}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}

function MetricCard({ label, value, format = '', suffix = '' }: any) {
  if (value === undefined || value === null) return null;
  
  let displayValue = value;
  if (typeof value === 'number' && format) {
    if (format === 'percent') {
      displayValue = (value * 100).toFixed(1) + '%';
    } else {
      displayValue = value.toFixed(1);
    }
  }
  
  return (
    <div className="bg-white p-4 rounded-lg border border-gray-200">
      <p className="text-sm text-gray-600 mb-1">{label}</p>
      <p className="text-xl font-bold text-blue-600">
        {displayValue}{suffix}
      </p>
    </div>
  );
}