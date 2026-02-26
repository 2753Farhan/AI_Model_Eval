// lib/hooks/useEvaluation.ts
import { useState, useEffect, useCallback } from 'react';
import { evaluationApi } from '@/lib/api/evaluation';
import { Evaluation, EvaluationResult } from '@/lib/types';

export const useEvaluation = (evaluationId?: string) => {
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [results, setResults] = useState<EvaluationResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = useCallback(async () => {
    if (!evaluationId) return;
    try {
      const data = await evaluationApi.status(evaluationId);
      setEvaluation(data);
    } catch (err) {
      setError('Failed to fetch evaluation status');
    }
  }, [evaluationId]);

  const fetchResults = useCallback(async () => {
    if (!evaluationId) return;
    try {
      const data = await evaluationApi.results(evaluationId);
      setResults(data);
    } catch (err) {
      setError('Failed to fetch results');
    }
  }, [evaluationId]);

  const startEvaluation = useCallback(
    async (models: string[], datasetId: string = 'humaneval') => {
      setLoading(true);
      try {
        const { evaluation_id } = await evaluationApi.create({
          models,
          dataset_id: datasetId,
          config: { num_samples: 5, timeout: 30, strategies: ['zero_shot'] },
        });
        await evaluationApi.start(evaluation_id);
        return evaluation_id;
      } catch (err) {
        setError('Failed to start evaluation');
        throw err;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  useEffect(() => {
    if (!evaluationId) return;

    fetchStatus();
    const interval = setInterval(fetchStatus, 2000);

    return () => clearInterval(interval);
  }, [evaluationId, fetchStatus]);

  useEffect(() => {
    if (evaluation?.status === 'completed') {
      fetchResults();
    }
  }, [evaluation?.status, fetchResults]);

  return {
    evaluation,
    results,
    loading,
    error,
    startEvaluation,
    refresh: fetchStatus,
  };
};