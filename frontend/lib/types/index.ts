// lib/types/index.ts
export interface Model {
  model_id: string;
  provider: string;
  active: boolean;
  config?: Record<string, any>;
}

export interface Evaluation {
  evaluation_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  current_stage: string;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  model_ids: string[];
  config: EvaluationConfig;
}

export interface EvaluationConfig {
  num_samples: number;
  timeout: number;
  strategies: string[];
}

export interface EvaluationResult {
  problem_id: string;
  task_id: string;
  passed: boolean;
  time_ms: number;
  output?: string;
  metrics?: Record<string, number>;
  test_results?: TestResult[];
}

export interface TestResult {
  test_id: number;
  passed: boolean;
  message: string;
}

export interface ComparisonData {
  model_id: string;
  model_name: string;
  pass_rate: number;
  avg_time_ms: number;
  total_tests: number;
  passed_tests: number;
  metrics: Record<string, number>;
}

export interface Report {
  report_id: string;
  evaluation_id: string;
  created_at: string;
  summary: ReportSummary;
  results: EvaluationResult[];
}

export interface ReportSummary {
  total: number;
  passed: number;
  failed: number;
  pass_rate: string;
}

export interface PlaygroundRequest {
  code: string;
  test_cases?: TestCase[];
  language?: string;
}

export interface TestCase {
  assertion: string;
}

export interface PlaygroundResponse {
  passed: boolean;
  output?: string;
  execution_time_ms: number;
  test_results?: TestResult[];
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
  
  // Per-function metrics
  function_metrics?: Array<{
    name: string;
    line: number;
    complexity: number;
    lines: number;
  }>;
}

export interface MetricsComparison {
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
}