// lib/hooks/usePlayground.ts
import { useState, useCallback } from 'react';
import { playgroundApi, MetricsResponse, CompareResponse, CodeMetrics } from '@/lib/api/playground';
import { PlaygroundResponse, TestCase } from '@/lib/types';

export const usePlayground = () => {
  const [code, setCode] = useState<string>('# Write your Python code here\n\ndef solution():\n    return "Hello World"');
  const [testCases, setTestCases] = useState<TestCase[]>([
    { assertion: 'assert solution() == "Hello World"' },
  ]);
  const [result, setResult] = useState<PlaygroundResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Metrics states
  const [metrics, setMetrics] = useState<CodeMetrics | null>(null);
  const [metricsLoading, setMetricsLoading] = useState(false);
  const [metricsError, setMetricsError] = useState<string | null>(null);
  const [comparisonResult, setComparisonResult] = useState<CompareResponse['comparison'] | null>(null);
  const [comparisonCode, setComparisonCode] = useState('');

  const runCode = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await playgroundApi.analyze({
        code,
        test_cases: testCases,
        language: 'python',
      });
      setResult(response);
    } catch (err) {
      setError('Failed to execute code');
    } finally {
      setLoading(false);
    }
  }, [code, testCases]);

  const analyzeMetrics = useCallback(async () => {
    if (!code.trim()) return;
    
    setMetricsLoading(true);
    setMetricsError(null);
    
    try {
      const response = await playgroundApi.getMetrics({
        code,
        language: 'python'
      });
      
      if (response.success) {
        setMetrics(response.metrics);
      } else {
        setMetricsError(response.error || 'Failed to analyze metrics');
      }
    } catch (err) {
      setMetricsError('Failed to connect to metrics service');
    } finally {
      setMetricsLoading(false);
    }
  }, [code]);

  const compareCode = useCallback(async () => {
    if (!code.trim() || !comparisonCode.trim()) return;
    
    setMetricsLoading(true);
    setMetricsError(null);
    
    try {
      const response = await playgroundApi.compare({
        code1: code,
        code2: comparisonCode,
        calculate_similarity: true
      });
      
      if (response.success) {
        setComparisonResult(response.comparison);
      } else {
        setMetricsError(response.error || 'Failed to compare code');
      }
    } catch (err) {
      setMetricsError('Failed to connect to metrics service');
    } finally {
      setMetricsLoading(false);
    }
  }, [code, comparisonCode]);

  const addTestCase = useCallback(() => {
    setTestCases((prev) => [...prev, { assertion: 'assert solution() ==' }]);
  }, []);

  const updateTestCase = useCallback((index: number, assertion: string) => {
    setTestCases((prev) => prev.map((tc, i) => (i === index ? { assertion } : tc)));
  }, []);

  const removeTestCase = useCallback((index: number) => {
    setTestCases((prev) => prev.filter((_, i) => i !== index));
  }, []);

  const resetComparison = useCallback(() => {
    setComparisonCode('');
    setComparisonResult(null);
  }, []);

  return {
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
    resetComparison,
  };
};