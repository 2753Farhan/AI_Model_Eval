// lib/hooks/useModels.ts
import { useState, useEffect } from 'react';
import { modelsApi } from '@/lib/api/models';
import { Model, ComparisonData } from '@/lib/types';

export const useModels = () => {
  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    const fetchModels = async () => {
      try {
        const data = await modelsApi.list();
        if (mounted) setModels(data);
      } catch (err) {
        if (mounted) setError('Failed to load models');
      } finally {
        if (mounted) setLoading(false);
      }
    };

    fetchModels();
    return () => {
      mounted = false;
    };
  }, []);

  const compareModels = async (modelIds: string[]): Promise<ComparisonData[]> => {
    try {
      return await modelsApi.compare(modelIds);
    } catch (err) {
      setError('Failed to compare models');
      return [];
    }
  };

  return { models, loading, error, compareModels };
};