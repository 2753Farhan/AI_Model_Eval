// app/reports/[id]/page.tsx
'use client';

import { useParams } from 'next/navigation';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Card } from '@/components/common/Card';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ResultsTable } from '@/components/evaluation/ResultsTable';

export default function ReportDetailPage() {
  const { id } = useParams();
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, fetch from API
    setTimeout(() => {
      setReport({
        report_id: id,
        evaluation_id: 'eval_123',
        created_at: new Date().toISOString(),
        summary: {
          total: 164,
          passed: 142,
          failed: 22,
          pass_rate: '86.6%',
        },
        results: Array.from({ length: 10 }, (_, i) => ({
          problem_id: `prob_${i}`,
          task_id: `HumanEval/${i}`,
          passed: Math.random() > 0.2,
          time_ms: Math.random() * 1000,
        })),
      });
      setLoading(false);
    }, 1000);
  }, [id]);

  if (loading) return <LoadingSpinner />;
  if (!report) return <div>Report not found</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Report Details</h1>
        <div className="space-x-4">
          <button
            onClick={() => window.print()}
            className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
          >
            🖨️ Print
          </button>
          <Link
            href={`/api/reports/${id}/download`}
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            ⬇️ Download
          </Link>
        </div>
      </div>

      {/* Report Metadata */}
      <Card className="mb-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-sm text-gray-500">Report ID</p>
            <p className="font-medium">{report.report_id}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Evaluation ID</p>
            <p className="font-medium">{report.evaluation_id}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Created</p>
            <p className="font-medium">
              {new Date(report.created_at).toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Format</p>
            <p className="font-medium">HTML</p>
          </div>
        </div>
      </Card>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <Card className="text-center">
          <p className="text-3xl font-bold text-blue-600">{report.summary.total}</p>
          <p className="text-sm text-gray-600">Total Tests</p>
        </Card>
        <Card className="text-center">
          <p className="text-3xl font-bold text-green-600">{report.summary.passed}</p>
          <p className="text-sm text-gray-600">Passed</p>
        </Card>
        <Card className="text-center">
          <p className="text-3xl font-bold text-red-600">{report.summary.failed}</p>
          <p className="text-sm text-gray-600">Failed</p>
        </Card>
        <Card className="text-center">
          <p className="text-3xl font-bold text-purple-600">
            {report.summary.pass_rate}
          </p>
          <p className="text-sm text-gray-600">Pass Rate</p>
        </Card>
      </div>

      {/* Results Table */}
      <Card title="Detailed Results">
        <ResultsTable results={report.results} />
      </Card>
    </div>
  );
}