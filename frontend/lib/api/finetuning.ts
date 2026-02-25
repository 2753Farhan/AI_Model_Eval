// lib/api/finetuning.ts
import { apiClient } from './client';

export interface FinetuningAnalysis {
  total_problems: number;
  total_failures: number;
  failure_rate: number;
  error_analysis: {
    by_type: Record<string, number>;
    most_common: Array<{ message: string; count: number }>;
  };
  patterns: any[];
  recommendations: string[];
  target_areas: Array<{
    type: string;
    name: string;
    count: number;
    priority: string;
  }>;
}

export interface TrainingDataResponse {
  success: boolean;
  training_file: string;
  failure_count: number;
  similar_problems: number;
}

export interface FinetuningJob {
  success: boolean;
  model?: string;
  status?: string;
  error?: string;
}

export const finetuningApi = {
  // Analyze evaluation for fine-tuning opportunities
  analyze: (evaluationId: string) =>
    apiClient.get<{ success: boolean; analysis: FinetuningAnalysis }>(
      `/finetuning/analyze/${evaluationId}`
    ),

  // List available datasets for fine-tuning
  listDatasets: () =>
    apiClient.get<any[]>('/finetuning/datasets'),

  // Prepare training data based on failures
  prepareTrainingData: (data: {
    evaluation_id: string;
    dataset_id?: string;
    max_problems?: number;
  }) =>
    apiClient.post<TrainingDataResponse>('/finetuning/prepare', data),

  // Start fine-tuning
  startFinetuning: (data: {
    base_model: string;
    training_file: string;
    output_model?: string;
  }) =>
    apiClient.post<FinetuningJob>('/finetuning/train', data),

  // List fine-tuned models
  listFinetunedModels: () =>
    apiClient.get<any[]>('/finetuning/models'),

  // Check fine-tuning status
  getStatus: (jobId: string) =>
    apiClient.get<any>(`/finetuning/status/${jobId}`),
};