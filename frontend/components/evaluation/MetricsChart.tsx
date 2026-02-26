// components/evaluation/MetricsChart.tsx
'use client';

import { EvaluationResult } from '@/lib/types';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface MetricsChartProps {
  results: EvaluationResult[];
}

export const MetricsChart = ({ results }: MetricsChartProps) => {
  // Safety check - ensure results is an array
  if (!results || !Array.isArray(results) || results.length === 0) {
    return (
      <div className="h-80 flex items-center justify-center text-gray-500">
        No data available
      </div>
    );
  }

  // Filter out invalid results and map safely
  const data = results
    .filter(r => r && typeof r === 'object') // Ensure each result is an object
    .map((r) => ({
      name: r.task_id ? r.task_id.slice(0, 10) : 'Unknown',
      time: r.time_ms || 0,
      passed: r.passed ? 1 : 0,
    }));

  if (data.length === 0) {
    return (
      <div className="h-80 flex items-center justify-center text-gray-500">
        No valid data for chart
      </div>
    );
  }

  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" angle={-45} textAnchor="end" height={60} />
          <YAxis yAxisId="left" />
          <YAxis yAxisId="right" orientation="right" />
          <Tooltip />
          <Bar yAxisId="left" dataKey="time" fill="#8884d8" name="Time (ms)" />
          <Bar yAxisId="right" dataKey="passed" fill="#82ca9d" name="Passed" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};