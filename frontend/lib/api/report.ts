// lib/types/report.ts
export interface ReportSummary {
  evaluation_id: string;
  created_at: string;
  duration: number;
  models: string[];
  total_results: number;
  passed_results: number;
  pass_rate: number;
  average_metrics: Record<string, number>;
  status: string;
}

export interface ModelStatistics {
  total: number;
  passed: number;
  pass_rate: number;
  avg_execution_time: number;
  error_count: number;
}

export interface ProblemStatistics {
  total_samples: number;
  passed_samples: number;
  by_model: Record<string, { total: number; passed: number }>;
}

export interface DetailedReportData {
  summary: ReportSummary;
  model_statistics: Record<string, ModelStatistics>;
  problem_statistics: Record<string, ProblemStatistics>;
  detailed_results: any[];
}

export interface ChartData {
  image: string;
  format: string;
}

export interface TableData {
  title: string;
  headers: string[];
  rows: (string | number)[][];
}

export interface BenchmarkRanking {
  rank: number;
  model: string;
  model_name: string;
  score: number;
  pass1: number;
  pass5: number;
  codebleu: number;
}

export interface ComparativeReportData {
  evaluations: Array<{
    evaluation_id: string;
    created_at: string;
    config: any;
  }>;
  benchmark: {
    benchmark_id: string;
    name: string;
    description: string;
    rankings: Record<string, number>;
    scores: Record<string, number>;
  };
  model_comparison: Record<
    string,
    {
      evaluations: Record<
        string,
        {
          total: number;
          passed: number;
          pass_rate: number;
          avg_execution_time: number;
          metrics: Record<string, number>;
        }
      >;
      aggregate: {
        total_results: number;
        passed_results: number;
        pass_rate: number;
        avg_execution_time: number;
        metrics: Record<string, number>;
      };
    }
  >;
}