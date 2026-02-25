// lib/api/evaluation.ts
import { apiClient } from './client';
import { Evaluation, EvaluationResult, Report } from '@/lib/types';

export const evaluationApi = {
  list: () => apiClient.get<Evaluation[]>('/evaluations'),

  create: (data: { models: string[]; dataset_id: string; config?: any }) =>
    apiClient.post<{ evaluation_id: string }>('/evaluations', data),

  start: (evaluationId: string) =>
    apiClient.post<{ status: string }>(`/evaluations/${evaluationId}/start`),

  status: (evaluationId: string) =>
    apiClient.get<Evaluation>(`/evaluations/${evaluationId}/status`),

  results: (evaluationId: string) =>
    apiClient.get<EvaluationResult[]>(`/evaluations/${evaluationId}/results`),

  report: (evaluationId: string, format: string = 'html') =>
    apiClient.post<{ report_id: string; download_url: string }>(
      `/evaluations/${evaluationId}/report`,
      { format }
    ),
};