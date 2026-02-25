// components/evaluation/ResultsTable.tsx
import { EvaluationResult } from '@/lib/types';

interface ResultsTableProps {
  results: EvaluationResult[];
}

export const ResultsTable = ({ results }: ResultsTableProps) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Problem
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Status
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Time (ms)
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Output
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {results.map((result) => (
            <tr key={result.problem_id}>
              <td className="px-6 py-4 whitespace-nowrap text-sm">
                {result.task_id}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                {result.passed ? (
                  <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded">
                    ✅ Passed
                  </span>
                ) : (
                  <span className="px-2 py-1 text-xs bg-red-100 text-red-800 rounded">
                    ❌ Failed
                  </span>
                )}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm">
                {result.time_ms ? result.time_ms.toFixed(2) : 'N/A'}
              </td>
              <td className="px-6 py-4 text-sm text-gray-500 max-w-md truncate">
                {result.output || '-'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};