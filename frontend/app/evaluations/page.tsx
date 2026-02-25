// app/evaluations/page.tsx
'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Card } from '@/components/common/Card';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { evaluationApi } from '@/lib/api/evaluation';

export default function EvaluationsPage() {
  const [evaluations, setEvaluations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEvals = async () => {
      try {
        const data = await evaluationApi.list();
        setEvaluations(data);
      } catch (err) {
        console.error('Failed to fetch evaluations:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchEvals();
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Evaluations</h1>
        <Link
          href="/evaluations/new"
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          New Evaluation
        </Link>
      </div>

      {evaluations.length === 0 ? (
        <Card>
          <p className="text-center text-gray-500 py-8">
            No evaluations yet.{' '}
            <Link href="/evaluations/new" className="text-blue-600 hover:underline">
              Start your first evaluation
            </Link>
          </p>
        </Card>
      ) : (
        <div className="space-y-4">
          {evaluations.map((evalItem) => (
            <Link
              key={evalItem.evaluation_id}
              href={`/evaluations/${evalItem.evaluation_id}`}
            >
              <Card className="hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-lg">
                      {evalItem.evaluation_id}
                    </h3>
                    <p className="text-sm text-gray-500">
                      Created: {new Date(evalItem.created_at).toLocaleString()}
                    </p>
                    <p className="text-sm text-gray-500">
                      Models: {evalItem.models?.join(', ')}
                    </p>
                  </div>
                  <div className="text-right">
                    <span
                      className={`inline-block px-3 py-1 text-sm rounded-full ${evalItem.status === 'completed'
                          ? 'bg-green-100 text-green-800'
                          : evalItem.status === 'running'
                            ? 'bg-blue-100 text-blue-800'
                            : evalItem.status === 'failed'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-gray-100 text-gray-800'
                        }`}
                    >
                      {evalItem.status}
                    </span>
                    {evalItem.status === 'running' && (
                      <div className="mt-2">
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-blue-500 h-2 rounded-full"
                            style={{ width: `${evalItem.progress}%` }}
                          />
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}