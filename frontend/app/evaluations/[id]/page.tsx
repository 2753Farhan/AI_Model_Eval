// app/evaluations/[id]/page.tsx
'use client';

import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { evaluationApi } from '@/lib/api/evaluation';
import { Card } from '@/components/common/Card';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ResultsTable } from '@/components/evaluation/ResultsTable';
import { MetricsChart } from '@/components/evaluation/MetricsChart';

export default function EvaluationDetailPage() {
  const { id } = useParams();
  const [evaluation, setEvaluation] = useState<any>(null);
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const status = await evaluationApi.status(id as string);
        setEvaluation(status);

        if (status.status === 'completed') {
          const results = await evaluationApi.results(id as string);
          setResults(results);
        }
      } catch (error) {
        console.error('Failed to fetch evaluation:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, [id]);

  if (loading) return <LoadingSpinner />;
  if (!evaluation) return <div>Evaluation not found</div>;

  const passedCount = results.filter((r) => r.passed).length;
  const passRate = results.length > 0 ? (passedCount / results.length) * 100 : 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">
        Evaluation: {id}
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <Card className="text-center">
          <p className="text-2xl font-bold text-blue-600">{evaluation.status}</p>
          <p className="text-sm text-gray-600">Status</p>
        </Card>
        <Card className="text-center">
          <p className="text-2xl font-bold text-green-600">{passedCount}</p>
          <p className="text-sm text-gray-600">Passed</p>
        </Card>
        <Card className="text-center">
          <p className="text-2xl font-bold text-red-600">{results.length - passedCount}</p>
          <p className="text-sm text-gray-600">Failed</p>
        </Card>
        <Card className="text-center">
          <p className="text-2xl font-bold text-purple-600">{passRate.toFixed(1)}%</p>
          <p className="text-sm text-gray-600">Pass Rate</p>
        </Card>
      </div>

      {evaluation.status === 'running' && (
        <Card title="Progress" className="mb-8">
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div
              className="bg-blue-500 h-4 rounded-full transition-all duration-500"
              style={{ width: `${evaluation.progress}%` }}
            />
          </div>
          <p className="text-right text-sm text-gray-500 mt-2">
            {evaluation.progress}% - {evaluation.current_stage}
          </p>
        </Card>
      )}

      {results.length > 0 && (
        <>
          <Card title="Results Overview" className="mb-8">
            <MetricsChart results={results} />
          </Card>

          <Card title="Detailed Results">
            <ResultsTable results={results} />
          </Card>
        </>
      )}
    </div>
  );
}