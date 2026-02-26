// lib/hooks/useDatasetSample.ts
import { useState, useCallback } from 'react';
import { datasetsApi, DatasetSampleDetail, ExecutionResult } from '@/lib/api/datasets';

export const useDatasetSample = (datasetId: string = 'humaneval') => {
  const [sample, setSample] = useState<DatasetSampleDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [executionResult, setExecutionResult] = useState<ExecutionResult | null>(null);
  const [metrics, setMetrics] = useState<any>(null);
  const [executing, setExecuting] = useState(false);

  const fetchSample = useCallback(async (sampleId: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await datasetsApi.getSample(datasetId, sampleId);
      setSample(data);
    } catch (err) {
      setError('Failed to load sample');
    } finally {
      setLoading(false);
    }
  }, [datasetId]);

  const executeSolution = useCallback(async (sampleId: string) => {
    setExecuting(true);
    setError(null);
    try {
      const result = await datasetsApi.executeSample(datasetId, sampleId);
      setExecutionResult(result);
      return result;
    } catch (err) {
      setError('Failed to execute solution');
      return null;
    } finally {
      setExecuting(false);
    }
  }, [datasetId]);

  const analyzeMetrics = useCallback(async (sampleId: string) => {
    setLoading(true);
    setError(null);
    try {
      const result = await datasetsApi.analyzeMetrics(datasetId, sampleId);
      setMetrics(result);
      return result;
    } catch (err) {
      setError('Failed to analyze metrics');
      return null;
    } finally {
      setLoading(false);
    }
  }, [datasetId]);

  const testCustomCode = useCallback(async (sampleId: string, code: string) => {
    setExecuting(true);
    setError(null);
    try {
      const result = await datasetsApi.testWithCustomCode(datasetId, sampleId, code);
      setExecutionResult(result);
      return result;
    } catch (err) {
      setError('Failed to test custom code');
      return null;
    } finally {
      setExecuting(false);
    }
  }, [datasetId]);

  return {
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
  };
};