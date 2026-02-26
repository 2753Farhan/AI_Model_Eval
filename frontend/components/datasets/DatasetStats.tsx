// components/datasets/DatasetStats.tsx
'use client';

import { Card } from '@/components/common/Card';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

interface DatasetStatsProps {
  stats: {
    total: number;
    by_difficulty: Record<string, number>;
    by_language: Record<string, number>;
    avg_complexity: number;
  };
}

export const DatasetStats = ({ stats }: DatasetStatsProps) => {
  const difficultyData = Object.entries(stats.by_difficulty || {}).map(([name, value]) => ({
    name,
    value,
  }));

  const languageData = Object.entries(stats.by_language || {}).map(([name, value]) => ({
    name,
    value,
  }));

  const COLORS = ['#10b981', '#f59e0b', '#ef4444', '#3b82f6', '#8b5cf6'];

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="text-center">
          <p className="text-3xl font-bold text-blue-600">{stats.total}</p>
          <p className="text-sm text-gray-600">Total Samples</p>
        </Card>
        <Card className="text-center">
          <p className="text-3xl font-bold text-purple-600">
            {stats.avg_complexity?.toFixed(2)}
          </p>
          <p className="text-sm text-gray-600">Avg Complexity</p>
        </Card>
        <Card className="text-center">
          <p className="text-3xl font-bold text-green-600">
            {Object.keys(stats.by_language || {}).length}
          </p>
          <p className="text-sm text-gray-600">Languages</p>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Difficulty Distribution */}
        <Card title="Difficulty Distribution">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={difficultyData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {difficultyData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Language Distribution */}
        <Card title="Languages">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={languageData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
};