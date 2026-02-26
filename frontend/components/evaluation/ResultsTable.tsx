// components/evaluation/ResultsTable.tsx
import { EvaluationResult } from '@/lib/types';

interface ResultsTableProps {
  results: EvaluationResult[];
}

export const ResultsTable = ({ results }: ResultsTableProps) => {
  if (!results || results.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No results available
      </div>
    );
  }

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
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Metrics
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {results.map((result, index) => {
            // Create a unique key using task_id (which should be unique per problem)
            // Since we might have multiple samples, add index as fallback
            const uniqueKey = `${result.task_id}-${index}`;
            
            return (
              <tr key={uniqueKey} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {result.task_id || 'Unknown'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {result.passed ? (
                    <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">
                      ✅ Passed
                    </span>
                  ) : (
                    <span className="px-2 py-1 text-xs bg-red-100 text-red-800 rounded-full">
                      ❌ Failed
                    </span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {result.time_ms ? result.time_ms.toFixed(2) : 'N/A'}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500 max-w-md truncate">
                  {result.output || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {result.metrics ? (
                    <span className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded">
                      {Object.keys(result.metrics).length} metrics
                    </span>
                  ) : (
                    '-'
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};