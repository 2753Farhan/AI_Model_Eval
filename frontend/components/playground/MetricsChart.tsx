// components/playground/MetricsChart.tsx
'use client';

import { CodeMetrics } from '@/lib/types';
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell
} from 'recharts';

interface MetricsChartProps {
  metrics: CodeMetrics;
}

export const MetricsChart = ({ metrics }: MetricsChartProps) => {
  // Radar chart data
  const radarData = [
    {
      metric: 'Maintainability',
      value: (metrics.maintainability_index || 0) / 100,
      fullMark: 1,
    },
    {
      metric: 'CodeBLEU',
      value: metrics.codebleu || 0,
      fullMark: 1,
    },
    {
      metric: 'Complexity',
      value: Math.max(0, 1 - ((metrics.cyclomatic_complexity || 0) / 20)),
      fullMark: 1,
    },
    {
      metric: 'Cognitive',
      value: Math.max(0, 1 - ((metrics.cognitive_complexity || 0) / 30)),
      fullMark: 1,
    },
  ].filter(item => item.value > 0);

  // Bar chart data for function complexities
  const functionData = metrics.function_metrics?.map(f => ({
    name: f.name,
    complexity: f.complexity,
    lines: f.lines,
  })) || [];

  const getComplexityColor = (value: number) => {
    if (value <= 5) return '#10b981';
    if (value <= 10) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="space-y-6">
      {radarData.length > 0 && (
        <div className="bg-white p-4 rounded-lg border border-border">
          <h3 className="text-sm font-medium text-secondary mb-4">Quality Radar</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="metric" />
                <PolarRadiusAxis angle={30} domain={[0, 1]} />
                <Radar
                  name="Code Quality"
                  dataKey="value"
                  stroke="#3b82f6"
                  fill="#3b82f6"
                  fillOpacity={0.6}
                />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {functionData.length > 0 && (
        <div className="bg-white p-4 rounded-lg border border-border">
          <h3 className="text-sm font-medium text-secondary mb-4">Function Complexity Breakdown</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={functionData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="complexity" name="Cyclomatic Complexity">
                  {functionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={getComplexityColor(entry.complexity)} />
                  ))}
                </Bar>
                <Bar dataKey="lines" name="Lines of Code" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
};