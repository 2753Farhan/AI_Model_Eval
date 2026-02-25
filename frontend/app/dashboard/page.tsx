// app/dashboard/page.tsx
'use client';

import { useState, useMemo, useEffect } from 'react';
import Link from 'next/link';
import { Card } from '@/components/common/Card';
import { StatCard } from '@/components/common/StatCard';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { useModels } from '@/lib/hooks/useModels';
import { evaluationApi } from '@/lib/api/evaluation';

export default function Dashboard() {
  const { models, loading: modelsLoading } = useModels();

  const [evaluations, setEvaluations] = useState<any[]>([]);
  const [evalsLoading, setEvalsLoading] = useState(true);

  useEffect(() => {
    const fetchEvals = async () => {
      try {
        const data = await evaluationApi.list();
        setEvaluations(data);
      } catch (err) {
        console.error('Failed to fetch evaluations:', err);
      } finally {
        setEvalsLoading(false);
      }
    };
    fetchEvals();
  }, []);

  const stats = useMemo(() => {
    const completed = evaluations.filter((e: any) => e.status === 'completed');
    return {
      totalEvals: evaluations.length,
      completedEvals: completed.length,
      totalModels: models.length,
    };
  }, [evaluations, models]);

  const recentEvals = useMemo(() => {
    return [...evaluations].slice(-5).reverse();
  }, [evaluations]);

  if (modelsLoading || evalsLoading) return <LoadingSpinner />;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-primary mb-8">Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <StatCard value={stats.totalEvals} label="Total Evaluations" color="blue" />
        <StatCard value={stats.completedEvals} label="Completed" color="green" />
        <StatCard value={stats.totalModels} label="Available Models" color="purple" />
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Link href="/evaluations/new" className="no-underline">
          <Card className="text-center hover:border-blue-200">
            <div className="text-3xl mb-2">📊</div>
            <h3 className="font-semibold text-primary">New Evaluation</h3>
            <p className="text-sm text-muted mt-1">Start a new model evaluation</p>
          </Card>
        </Link>

        <Link href="/playground" className="no-underline">
          <Card className="text-center hover:border-green-200">
            <div className="text-3xl mb-2">💻</div>
            <h3 className="font-semibold text-primary">Playground</h3>
            <p className="text-sm text-muted mt-1">Test code in sandbox</p>
          </Card>
        </Link>

        <Link href="/models/compare" className="no-underline">
          <Card className="text-center hover:border-purple-200">
            <div className="text-3xl mb-2">⚖️</div>
            <h3 className="font-semibold text-primary">Compare Models</h3>
            <p className="text-sm text-muted mt-1">Compare model performance</p>
          </Card>
        </Link>
      </div>

      {/* Recent Evaluations */}
      <Card title="Recent Evaluations">
        {recentEvals.length === 0 ? (
          <p className="text-muted text-center py-8">No recent evaluations</p>
        ) : (
          <div className="space-y-3">
            {recentEvals.map((evalItem) => (
              <Link
                key={evalItem.evaluation_id}
                href={`/evaluations/${evalItem.evaluation_id}`}
                className="block p-4 border border-border rounded-lg hover:bg-gray-50 transition-colors no-underline"
              >
                <div className="flex justify-between items-center">
                  <div>
                    <p className="font-medium text-primary">
                      {evalItem.evaluation_id.slice(0, 8)}...
                    </p>
                    <p className="text-sm text-secondary">
                      Status: <span className="capitalize">{evalItem.status}</span>
                    </p>
                  </div>
                  <div className="flex items-center space-x-4">
                    {evalItem.status === 'running' && (
                      <div className="w-24">
                        <div className="progress-bar">
                          <div
                            className="progress-bar-fill"
                            style={{ width: `${evalItem.progress}%` }}
                          />
                        </div>
                      </div>
                    )}
                    <span className={`badge ${evalItem.status === 'completed' ? 'badge-success' :
                        evalItem.status === 'running' ? 'badge-info' :
                          evalItem.status === 'failed' ? 'badge-error' : 'badge-warning'
                      }`}>
                      {evalItem.progress}%
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}