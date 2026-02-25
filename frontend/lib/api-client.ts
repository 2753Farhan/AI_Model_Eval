// frontend/lib/api-client.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001/api';

export interface Model {
  model_id: string;
  provider: string;
  active: boolean;
}

export interface Evaluation {
  evaluation_id: string;
  status: string;
  progress: number;
}

export interface EvaluationResult {
  problem_id: string;
  task_id: string;
  passed: boolean;
  time_ms: number;
}

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    // Simple fetch without credentials
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }

  async listModels() {
    return this.request<Model[]>('/models');
  }

  async listDatasets() {
    return this.request<any[]>('/datasets');
  }

  async createEvaluation(data: { models: string[]; dataset_id: string }) {
    return this.request<{ evaluation_id: string }>('/evaluations', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async startEvaluation(evaluationId: string) {
    return this.request<{ status: string }>(`/evaluations/${evaluationId}/start`, {
      method: 'POST',
    });
  }

  async getEvaluationStatus(evaluationId: string) {
    return this.request<Evaluation>(`/evaluations/${evaluationId}/status`);
  }

  async getResults(evaluationId: string) {
    return this.request<EvaluationResult[]>(`/evaluations/${evaluationId}/results`);
  }
}

export const apiClient = new ApiClient();