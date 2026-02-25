// app/page.tsx
import Link from 'next/link';

export default function Home() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
          AI Model Evaluation
        </h1>
        <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
          Evaluate, compare, and analyze AI code generation models with our comprehensive framework.
        </p>
        <div className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
          <div className="rounded-md shadow">
            <Link
              href="/dashboard"
              className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10"
            >
              Get Started
            </Link>
          </div>
        </div>
      </div>

      <div className="mt-16 grid grid-cols-1 gap-8 md:grid-cols-3">
        {features.map((feature) => (
          <div key={feature.title} className="bg-white rounded-lg shadow-sm p-6">
            <div className="text-3xl mb-4">{feature.icon}</div>
            <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
            <p className="text-gray-600">{feature.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

const features = [
  {
    icon: '🤖',
    title: 'Multi-Model Support',
    description: 'Test multiple AI models side by side including Ollama and HuggingFace.',
  },
  {
    icon: '📊',
    title: 'Comprehensive Metrics',
    description: 'Pass@k, execution time, code quality, and semantic similarity metrics.',
  },
  {
    icon: '💻',
    title: 'Code Playground',
    description: 'Test and validate your own Python code with our evaluation engine.',
  },
  {
    icon: '📈',
    title: 'Detailed Reports',
    description: 'Generate and download HTML, PDF, or CSV reports of your evaluations.',
  },
  {
    icon: '⚖️',
    title: 'Model Comparison',
    description: 'Compare performance metrics across different models.',
  },
  {
    icon: '🔍',
    title: 'Error Analysis',
    description: 'Detailed error analysis and pattern detection.',
  },
];