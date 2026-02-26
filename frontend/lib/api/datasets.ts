// lib/api/datasets.ts
import { apiClient } from './client';

export interface DatasetInfo {
  id: string;
  name: string;
  description: string;
  source: string;
  paper: string;
  year: number;
  total_problems: number;
  languages: Record<string, number>;
  difficulties: {
    easy: number;
    medium: number;
    hard: number;
  };
  avg_test_cases: number;
  total_test_cases: number;
  license: string;
  citation: string;
}

export interface DatasetSummary {
  id: string;
  name: string;
  description: string;
  problems: number;
}

export interface DatasetSample {
  problem_id: string;
  task_id: string;
  entry_point: string;
  prompt_preview: string;
  difficulty: string;
  test_count: number;
  language: string;
  metrics: Record<string, any>;
  has_solution: boolean;
}

export interface DatasetSampleDetail extends DatasetSample {
  prompt: string;
  canonical_solution: string;
  test_code: string;
  test_cases: Array<{
    assertion: string;
    type: string;
    description: string;
  }>;
  tags: string[];
  stats: Record<string, any>;
}

export interface DatasetStatistics {
  total_problems: number;
  languages: Record<string, number>;
  difficulties: {
    easy: number;
    medium: number;
    hard: number;
  };
  test_cases: {
    total: number;
    avg_per_problem: number;
    distribution: number[];
  };
  complexity: {
    avg_cyclomatic: number;
    avg_lines: number;
    distribution: {
      min: number;
      max: number;
      median: number;
    };
  };
  categories: Record<string, number>;
  solution_stats: {
    has_solution: number;
    avg_solution_length: number;
    total_solutions: number;
  };
}

export interface ExecutionResult {
  passed: boolean;
  output?: string;
  execution_time_ms: number;
  test_results?: Array<{
    passed: boolean;
    message: string;
  }>;
  error?: string;
  task_id?: string;
  entry_point?: string;
}

export interface SearchResult {
  query: string;
  total_results: number;
  results: Array<{
    problem_id: string;
    task_id: string;
    entry_point: string;
    prompt_preview: string;
    relevance_score: number;
    test_count: number;
    difficulty: string;
  }>;
}

export const datasetsApi = {
  // List all available datasets
  list: () => apiClient.get<DatasetSummary[]>('/datasets'),

  // Get detailed info about a specific dataset
  getInfo: (datasetId: string) => 
    apiClient.get<DatasetInfo>(`/datasets/${datasetId}`),
  
  // Get paginated samples from a dataset
  getSamples: (datasetId: string, limit: number = 50, offset: number = 0) =>
    apiClient.get<{ total: number; offset: number; limit: number; samples: DatasetSample[] }>(
      `/datasets/${datasetId}/samples?limit=${limit}&offset=${offset}`
    ),
  
  // Get a single sample by ID
  getSample: (datasetId: string, sampleId: string) =>
    apiClient.get<DatasetSampleDetail>(`/datasets/${datasetId}/samples/${sampleId}`),
  
  // Get dataset statistics
  getStatistics: (datasetId: string) =>
    apiClient.get<DatasetStatistics>(`/datasets/${datasetId}/stats`),
  
  // Search samples in a dataset
  search: (datasetId: string, query: string) =>
    apiClient.get<SearchResult>(`/datasets/${datasetId}/search?q=${encodeURIComponent(query)}`),
  
  // Execute a sample's canonical solution
  executeSample: (datasetId: string, sampleId: string) =>
    apiClient.post<ExecutionResult>(`/datasets/${datasetId}/samples/${sampleId}/execute`, {}),
  
  // Analyze metrics for a sample
  analyzeMetrics: (datasetId: string, sampleId: string) =>
    apiClient.post<any>(`/datasets/${datasetId}/samples/${sampleId}/metrics`, {}),
  
  // Test custom code against a sample's test cases
  testWithCustomCode: (datasetId: string, sampleId: string, code: string) =>
    apiClient.post<ExecutionResult>(`/datasets/${datasetId}/samples/${sampleId}/test`, { code }),
  
  // Get a random sample
  getRandomSample: (datasetId: string) =>
    apiClient.get<{ problem_id: string; task_id: string; entry_point: string; prompt_preview: string; difficulty: string; test_count: number }>(
      `/datasets/${datasetId}/random`
    ),
};