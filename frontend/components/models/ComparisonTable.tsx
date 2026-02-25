// components/models/ComparisonTable.tsx
import { ComparisonData } from '@/lib/types';

interface ComparisonTableProps {
  data: ComparisonData[];
}

export const ComparisonTable = ({ data }: ComparisonTableProps) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Model
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Pass Rate
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Avg Time (ms)
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Tests Passed
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              CodeBLEU
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((model) => (
            <tr key={model.model_id}>
              <td className="px-6 py-4 whitespace-nowrap font-medium">
                {model.model_name}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span
                  className={`px-2 py-1 text-xs rounded ${
                    model.pass_rate > 0.7
                      ? 'bg-green-100 text-green-800'
                      : model.pass_rate > 0.4
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-red-100 text-red-800'
                  }`}
                >
                  {(model.pass_rate * 100).toFixed(1)}%
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                {model.avg_time_ms.toFixed(2)}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                {model.passed_tests}/{model.total_tests}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                {model.metrics?.codebleu
                  ? (model.metrics.codebleu * 100).toFixed(1) + '%'
                  : 'N/A'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};