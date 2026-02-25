// lib/hooks/useDataset.ts
import { useState, useEffect, useCallback } from 'react';
import { datasetsApi, DatasetSample, DatasetInfo } from '@/lib/api/datasets';

export const useDataset = (datasetId: string = 'humaneval') => {
  const [info, setInfo] = useState<DatasetInfo | null>(null);
  const [samples, setSamples] = useState<DatasetSample[]>([]);
  const [selectedSample, setSelectedSample] = useState<DatasetSample | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState<any>(null);
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 20,
    total: 0,
  });

  // Fetch dataset info
  useEffect(() => {
    const fetchInfo = async () => {
      try {
        const data = await datasetsApi.list();
        const dataset = data.find(d => d.id === datasetId);
        setInfo(dataset || null);
      } catch (err) {
        setError('Failed to fetch dataset info');
      }
    };
    fetchInfo();
  }, [datasetId]);

  // Fetch samples
  const fetchSamples = useCallback(async (page: number = pagination.page) => {
    setLoading(true);
    try {
      const offset = (page - 1) * pagination.limit;
      const data = await datasetsApi.getSamples(datasetId, pagination.limit, offset);
      setSamples(data.samples);
      setPagination(prev => ({ ...prev, total: data.total, page }));
    } catch (err) {
      setError('Failed to fetch samples');
    } finally {
      setLoading(false);
    }
  }, [datasetId, pagination.limit]);

  // Fetch stats
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await datasetsApi.getStats(datasetId);
        setStats(data);
      } catch (err) {
        console.error('Failed to fetch stats:', err);
      }
    };
    fetchStats();
  }, [datasetId]);

  // Fetch single sample
  const fetchSample = useCallback(async (sampleId: string) => {
    try {
      const data = await datasetsApi.getSample(datasetId, sampleId);
      setSelectedSample(data);
      return data;
    } catch (err) {
      setError('Failed to fetch sample');
      return null;
    }
  }, [datasetId]);

  // Search samples
  const searchSamples = useCallback(async (query: string) => {
    if (!query) {
      fetchSamples(1);
      return;
    }
    setLoading(true);
    try {
      const data = await datasetsApi.search(datasetId, query);
      setSamples(data);
      setPagination(prev => ({ ...prev, total: data.length }));
    } catch (err) {
      setError('Search failed');
    } finally {
      setLoading(false);
    }
  }, [datasetId, fetchSamples]);

  useEffect(() => {
    fetchSamples(1);
  }, [fetchSamples]);

  return {
    info,
    samples,
    selectedSample,
    loading,
    error,
    stats,
    pagination,
    fetchSamples,
    fetchSample,
    searchSamples,
    setSelectedSample,
  };
};