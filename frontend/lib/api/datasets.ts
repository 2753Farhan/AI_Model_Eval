// lib/api/datasets.ts
import { apiClient } from './client';

export interface DatasetSample {
  task_id: string;
  prompt: string;
  canonical_solution: string;
  test: string;
  entry_point: string;
  difficulty?: string;
  tags?: string[];
}

export interface DatasetInfo {
  id: string;
  name: string;
  description: string;
  total_samples: number;
  languages: string[];
  source: string;
}

export const datasetsApi = {
  // Get all datasets info
  list: () => apiClient.get<DatasetInfo[]>('/datasets'),

  // Get samples for a dataset
  getSamples: (datasetId: string, limit?: number, offset?: number) =>
    apiClient.get<{ samples: DatasetSample[]; total: number }>(
      `/datasets/${datasetId}/samples?limit=${limit || 50}&offset=${offset || 0}`
    ),

  // Get a single sample
  getSample: (datasetId: string, sampleId: string) =>
    apiClient.get<DatasetSample>(`/datasets/${datasetId}/samples/${sampleId}`),

  // Get dataset statistics
  getStats: (datasetId: string) =>
    apiClient.get<{
      total: number;
      by_difficulty: Record<string, number>;
      by_language: Record<string, number>;
      avg_complexity: number;
    }>(`/datasets/${datasetId}/stats`),

  // Search samples
  search: (datasetId: string, query: string) =>
    apiClient.get<DatasetSample[]>(`/datasets/${datasetId}/search?q=${encodeURIComponent(query)}`),
};