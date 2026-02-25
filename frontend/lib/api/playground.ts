// lib/api/playground.ts
import { apiClient } from './client';
import { PlaygroundRequest, PlaygroundResponse } from '@/lib/types';

export interface MetricsRequest {
  code: string;
  language?: string;
  reference?: string;
}

export interface MetricsResponse {
  success: boolean;
  language: string;
  metrics: CodeMetrics;
  summary?: string;
  error?: string;
}

export interface CodeMetrics {
  // Quality metrics
  loc?: number;
  lloc?: number;
  comments?: number;
  cyclomatic_complexity?: number;
  maintainability_index?: number;
  cognitive_complexity?: number;
  quality_grade?: string;
  
  // Basic metrics
  total_lines?: number;
  blank_lines?: number;
  code_lines?: number;
  comment_lines?: number;
  function_count?: number;
  class_count?: number;
  import_count?: number;
  
  // Semantic metrics
  codebleu?: number;
}

export interface CompareRequest {
  code1: string;
  code2: string;
  language?: string;
  calculate_similarity?: boolean;
}

export interface CompareResponse {
  success: boolean;
  comparison: {
    code1: CodeMetrics;
    code2: CodeMetrics;
    similarity?: number;
    differences: Record<string, number>;
    better: 'code1' | 'code2' | 'equal';
    reason: string;
    scores?: {
      code1: number;
      code2: number;
    };
  };
  error?: string;
}

export interface BatchMetricsRequest {
  codes: string[];
}

export interface BatchMetricsResponse {
  success: boolean;
  results: Array<{
    index: number;
    metrics: CodeMetrics;
    summary: string;
  }>;
}

export const playgroundApi = {
  analyze: (data: PlaygroundRequest) =>
    apiClient.post<PlaygroundResponse>('/analyze', data),

  validate: (code: string) =>
    apiClient.post<{ valid: boolean; errors?: string[] }>('/validate', { code }),

  getMetrics: (data: MetricsRequest) =>
    apiClient.post<MetricsResponse>('/metrics/code', data),

  compare: (data: CompareRequest) =>
    apiClient.post<CompareResponse>('/metrics/compare', data),

  batchMetrics: (data: BatchMetricsRequest) =>
    apiClient.post<BatchMetricsResponse>('/metrics/batch', data),

  getMetricExplanation: (metricName: string) =>
    apiClient.get<any>(`/metrics/explain/${metricName}`),
};