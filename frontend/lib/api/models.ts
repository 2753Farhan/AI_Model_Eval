// lib/api/models.ts
import { apiClient } from './client';
import { Model, ComparisonData } from '@/lib/types';

export const modelsApi = {
  list: () => apiClient.get<Model[]>('/models'),

  compare: async (modelIds: string[]) => {
    const results = await Promise.all(
      modelIds.map(async (id) => {
        const model = await apiClient.get<Model>(`/models/${id}`);
        const stats = await apiClient.get<ComparisonData>(`/models/${id}/stats`);
        return { ...model, ...stats };
      })
    );
    return results;
  },
};