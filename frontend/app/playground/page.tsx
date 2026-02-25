// app/playground/page.tsx
'use client';

import { useState } from 'react';
import { usePlayground } from '@/lib/hooks/usePlayground';
import { Card } from '@/components/common/Card';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';

type TabType = 'code' | 'metrics' | 'comparison';

export default function PlaygroundPage() {
  const {
    // Code execution
    code,
    setCode,
    testCases,
    result,
    loading,
    error,
    runCode,
    addTestCase,
    updateTestCase,
    removeTestCase,
    
    // Metrics
    metrics,
    metricsLoading,
    metricsError,
    analyzeMetrics,
    
    // Comparison
    comparisonCode,
    setComparisonCode,
    comparisonResult,
    compareCode,
  } = usePlayground();

  const [activeTab, setActiveTab] = useState<TabType>('code');

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Code Playground</h1>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex space-x-8">
          <button
            onClick={() => setActiveTab('code')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'code'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            💻 Code & Test
          </button>
          <button
            onClick={() => {
              setActiveTab('metrics');
              if (!metrics && code) analyzeMetrics();
            }}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'metrics'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            📊 Code Metrics
          </button>
          <button
            onClick={() => setActiveTab('comparison')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'comparison'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            🔄 Compare Code
          </button>
        </nav>
      </div>

      {/* Code & Test Tab */}
      {activeTab === 'code' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Code Editor */}
          <Card title="Python Code">
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full h-64 p-4 font-mono text-sm border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50"
              placeholder="# Write your Python code here..."
            />
            <div className="mt-4 flex justify-end space-x-3">
              <button
                onClick={analyzeMetrics}
                className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 text-sm"
              >
                📊 Analyze Metrics
              </button>
            </div>
          </Card>

          {/* Test Cases */}
          <Card title="Test Cases">
            <div className="space-y-3">
              {testCases.map((testCase, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <input
                    type="text"
                    value={testCase.assertion}
                    onChange={(e) => updateTestCase(index, e.target.value)}
                    className="flex-1 p-2 text-sm font-mono border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50"
                    placeholder="assert solution() == ..."
                  />
                  <button
                    onClick={() => removeTestCase(index)}
                    className="p-2 text-red-600 hover:text-red-800"
                  >
                    ✕
                  </button>
                </div>
              ))}
              <button
                onClick={addTestCase}
                className="w-full py-2 border-2 border-dashed border-gray-300 rounded-md text-gray-500 hover:border-blue-500 hover:text-blue-500"
              >
                + Add Test Case
              </button>
            </div>
          </Card>

          {/* Run Button */}
          <div className="lg:col-span-2">
            <button
              onClick={runCode}
              disabled={loading}
              className="w-full py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 font-medium"
            >
              {loading ? 'Running...' : '▶ Run Code'}
            </button>
          </div>

          {/* Results */}
          {(result || error) && (
            <div className="lg:col-span-2">
              <Card title="Execution Results">
                {error && (
                  <div className="p-4 bg-red-50 border border-red-200 rounded-md">
                    <p className="text-red-700">{error}</p>
                  </div>
                )}

                {result && (
                  <div className="space-y-4">
                    <div
                      className={`p-4 rounded-md ${
                        result.passed ? 'bg-green-50' : 'bg-red-50'
                      }`}
                    >
                      <p className="font-semibold">
                        {result.passed ? '✅ All Tests Passed' : '❌ Tests Failed'}
                      </p>
                      <p className="text-sm text-gray-600">
                        Execution time: {result.execution_time_ms?.toFixed(2) || 0}ms
                      </p>
                    </div>

                    {result.test_results && result.test_results.length > 0 && (
                      <div>
                        <h3 className="font-semibold mb-2">Test Results</h3>
                        <div className="space-y-2">
                          {result.test_results.map((test: any, i: number) => (
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

                    {result.output && !result.passed && (
                      <div>
                        <h3 className="font-semibold mb-2">Error Output</h3>
                        <pre className="p-4 bg-gray-900 text-white rounded-md overflow-x-auto text-sm font-mono">
                          {result.output}
                        </pre>
                      </div>
                    )}
                  </div>
                )}
              </Card>
            </div>
          )}
        </div>
      )}

      {/* Metrics Tab */}
      {activeTab === 'metrics' && (
        <div className="space-y-6">
          {/* Code Preview */}
          <Card title="Code Being Analyzed">
            <pre className="bg-gray-900 text-gray-100 p-4 rounded-md overflow-x-auto text-sm font-mono max-h-60 overflow-y-auto">
              {code || 'No code to analyze'}
            </pre>
          </Card>

          {/* Metrics Display */}
          {metricsLoading ? (
            <LoadingSpinner />
          ) : metricsError ? (
            <Card>
              <div className="text-center py-8 text-red-600">
                <p className="text-lg mb-2">❌ {metricsError}</p>
                <button
                  onClick={analyzeMetrics}
                  className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Try Again
                </button>
              </div>
            </Card>
          ) : metrics ? (
            <Card>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                <MetricItem 
                  label="Lines of Code" 
                  value={metrics.loc || metrics.total_lines} 
                />
                <MetricItem 
                  label="Functions" 
                  value={metrics.function_count} 
                />
                <MetricItem 
                  label="Classes" 
                  value={metrics.class_count} 
                />
                <MetricItem 
                  label="Complexity" 
                  value={metrics.cyclomatic_complexity} 
                  format=".1f"
                />
                <MetricItem 
                  label="Maintainability" 
                  value={metrics.maintainability_index} 
                  format=".1f"
                  suffix="%"
                />
                <MetricItem 
                  label="Quality Grade" 
                  value={metrics.quality_grade} 
                />
              </div>
            </Card>
          ) : (
            <Card>
              <div className="text-center py-12 text-gray-500">
                <p className="text-lg mb-2">📊 No metrics to display</p>
                <p className="text-sm mb-4">Click  &quot Analyze Metrics &quot in the Code tab</p>
                <button
                  onClick={() => setActiveTab('code')}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Go to Code Tab
                </button>
              </div>
            </Card>
          )}
        </div>
      )}

      {/* Comparison Tab */}
      {activeTab === 'comparison' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Original Code */}
            <Card title="Original Code">
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className="w-full h-48 p-4 font-mono text-sm border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50"
                placeholder="# Original code..."
              />
            </Card>

            {/* Code to Compare */}
            <Card title="Code to Compare">
              <textarea
                value={comparisonCode}
                onChange={(e) => setComparisonCode(e.target.value)}
                className="w-full h-48 p-4 font-mono text-sm border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50"
                placeholder="# Code to compare with..."
              />
            </Card>
          </div>

          {/* Compare Button */}
          <div className="flex justify-center">
            <button
              onClick={compareCode}
              disabled={!code.trim() || !comparisonCode.trim() || metricsLoading}
              className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 font-medium"
            >
              {metricsLoading ? 'Comparing...' : '🔄 Compare Code'}
            </button>
          </div>

          {/* Comparison Results */}
          {comparisonResult && (
            <Card title="Comparison Results">
              <div className="space-y-4">
                {/* Winner Badge */}
                <div className={`p-4 rounded-lg text-center ${
                  comparisonResult.better === 'code1' ? 'bg-green-50' :
                  comparisonResult.better === 'code2' ? 'bg-blue-50' : 'bg-gray-50'
                }`}>
                  <p className="text-lg font-semibold">
                    {comparisonResult.better === 'code1' && '✅ Original Code is Better'}
                    {comparisonResult.better === 'code2' && '✅ Compared Code is Better'}
                    {comparisonResult.better === 'equal' && '⚖️ Both Codes are Similar'}
                  </p>
                  <p className="text-sm text-gray-600">{comparisonResult.reason}</p>
                </div>

                {/* Simple Comparison Table */}
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Metric</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Original</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Compared</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      <tr>
                        <td className="px-4 py-2 text-sm">Lines of Code</td>
                        <td className="px-4 py-2 text-sm">{comparisonResult.code1?.loc || 0}</td>
                        <td className="px-4 py-2 text-sm">{comparisonResult.code2?.loc || 0}</td>
                      </tr>
                      <tr>
                        <td className="px-4 py-2 text-sm">Complexity</td>
                        <td className="px-4 py-2 text-sm">{(comparisonResult.code1?.cyclomatic_complexity || 0).toFixed(1)}</td>
                        <td className="px-4 py-2 text-sm">{(comparisonResult.code2?.cyclomatic_complexity || 0).toFixed(1)}</td>
                      </tr>
                      <tr>
                        <td className="px-4 py-2 text-sm">Maintainability</td>
                        <td className="px-4 py-2 text-sm">{(comparisonResult.code1?.maintainability_index || 0).toFixed(1)}%</td>
                        <td className="px-4 py-2 text-sm">{(comparisonResult.code2?.maintainability_index || 0).toFixed(1)}%</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}

// Simple Metric Item Component
function MetricItem({ label, value, format = '', suffix = '' }: any) {
  if (value === undefined || value === null) return null;
  
  let displayValue = value;
  if (typeof value === 'number' && format) {
    displayValue = value.toFixed(1);
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