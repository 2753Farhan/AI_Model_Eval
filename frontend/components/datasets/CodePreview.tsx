// components/datasets/CodePreview.tsx
import { useState } from 'react';
import { Card } from '@/components/common/Card';

interface CodePreviewProps {
  code: string;
  language?: string;
  title?: string;
}

export const CodePreview = ({ code, language = 'python', title }: CodePreviewProps) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Card title={title}>
      <div className="relative">
        <button
          onClick={handleCopy}
          className="absolute top-2 right-2 px-3 py-1 text-xs bg-gray-700 text-white rounded hover:bg-gray-600 transition-colors"
        >
          {copied ? '✓ Copied!' : 'Copy'}
        </button>
        <pre className="bg-gray-900 text-gray-100 p-4 rounded-md overflow-x-auto text-sm font-mono max-h-96 overflow-y-auto">
          {code}
        </pre>
      </div>
    </Card>
  );
};