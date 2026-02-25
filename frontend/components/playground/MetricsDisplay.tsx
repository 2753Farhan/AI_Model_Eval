// components/playground/MetricsDisplay.tsx
'use client';

import { CodeMetrics } from '@/lib/types';
import { Card } from '@/components/common/Card';

interface MetricsDisplayProps {
  metrics: CodeMetrics;
}

export const MetricsDisplay = ({ metrics }: MetricsDisplayProps) => {
  const getQualityColor = (grade: string) => {
    switch(grade?.toLowerCase()) {
      case 'excellent': return 'text-green-600 bg-green-50';
      case 'good': return 'text-blue-600 bg-blue-50';
      case 'fair': return 'text-yellow-600 bg-yellow-50';
      case 'poor': return 'text-red-600 bg-red-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="space-y-6">
      {/* Quality Grade */}
      {metrics.quality_grade && (
        <div className={`p-4 rounded-lg text-center ${getQualityColor(metrics.quality_grade)}`}>
          <p className="text-sm font-medium">Code Quality</p>
          <p className="text-2xl font-bold">{metrics.quality_grade}</p>
        </div>
      )}

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard
          label="Lines of Code"
          value={metrics.loc || metrics.total_lines}
          format="number"
        />
        <MetricCard
          label="Code Lines"
          value={metrics.code_lines}
          format="number"
        />
        <MetricCard
          label="Comments"
          value={metrics.comments || metrics.comment_lines}
          format="number"
        />
        <MetricCard
          label="Functions"
          value={metrics.function_count}
          format="number"
        />
        <MetricCard
          label="Cyclomatic Complexity"
          value={metrics.cyclomatic_complexity}
          format="decimal"
          threshold={10}
        />
        <MetricCard
          label="Maintainability Index"
          value={metrics.maintainability_index}
          format="percent"
          threshold={60}
          reverse
        />
        <MetricCard
          label="Cognitive Complexity"
          value={metrics.cognitive_complexity}
          format="decimal"
          threshold={15}
        />
        <MetricCard
          label="CodeBLEU"
          value={metrics.codebleu}
          format="percent"
          threshold={0.8}
        />
      </div>

      {/* Function Details */}
      {metrics.function_metrics && metrics.function_metrics.length > 0 && (
        <Card title="Function Details">
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2 px-4 text-sm font-medium text-secondary">Function</th>
                  <th className="text-left py-2 px-4 text-sm font-medium text-secondary">Line</th>
                  <th className="text-left py-2 px-4 text-sm font-medium text-secondary">Lines</th>
                  <th className="text-left py-2 px-4 text-sm font-medium text-secondary">Complexity</th>
                </tr>
              </thead>
              <tbody>
                {metrics.function_metrics.map((func, i) => (
                  <tr key={i} className="border-b last:border-0">
                    <td className="py-2 px-4 text-sm font-mono">{func.name}</td>
                    <td className="py-2 px-4 text-sm">{func.line}</td>
                    <td className="py-2 px-4 text-sm">{func.lines}</td>
                    <td className="py-2 px-4 text-sm">
                      <span className={`px-2 py-1 rounded text-xs ${
                        func.complexity <= 5 ? 'bg-green-100 text-green-800' :
                        func.complexity <= 10 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {func.complexity}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}
    </div>
  );
};

interface MetricCardProps {
  label: string;
  value?: number;
  format?: 'number' | 'decimal' | 'percent';
  threshold?: number;
  reverse?: boolean;
}

const MetricCard = ({ label, value, format = 'number', threshold, reverse }: MetricCardProps) => {
  if (value === undefined || value === null) return null;

  const formattedValue = (() => {
    if (format === 'percent') return `${(value * 100).toFixed(1)}%`;
    if (format === 'decimal') return value.toFixed(2);
    return value.toString();
  })();

  const getStatusColor = () => {
    if (!threshold) return 'text-primary';
    
    if (reverse) {
      return value >= threshold ? 'text-green-600' : 'text-red-600';
    }
    return value <= threshold ? 'text-green-600' : 'text-red-600';
  };

  return (
    <div className="bg-white p-4 rounded-lg border border-border">
      <p className="text-sm text-secondary mb-1">{label}</p>
      <p className={`text-xl font-bold ${getStatusColor()}`}>{formattedValue}</p>
    </div>
  );
};