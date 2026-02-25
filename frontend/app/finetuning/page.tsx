// app/finetuning/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { Card } from '@/components/common/Card';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { finetuningApi } from '@/lib/api/finetuning';
import { useModels } from '@/lib/hooks/useModels';
import Link from 'next/link';

type Step = 'select-model' | 'select-evaluation' | 'analyze' | 'prepare' | 'train' | 'complete';

// Dataset options
const DATASETS = [
  {
    id: 'code_alpaca',
    name: 'Code Alpaca',
    description: '20,000 instruction-following examples for code generation',
    size: '20k',
    recommended: true,
    icon: '🦙',
    features: ['Python-focused', 'Diverse problems', 'High quality']
  },
  {
    id: 'codesearchnet',
    name: 'CodeSearchNet Python',
    description: '50,000 Python code examples with docstrings from GitHub',
    size: '50k',
    recommended: false,
    icon: '🔍',
    features: ['Real-world code', 'Comprehensive', 'Well-documented']
  },
  {
    id: 'humaneval',
    name: 'HumanEval',
    description: '164 hand-written programming problems from OpenAI',
    size: '164',
    recommended: false,
    icon: '📝',
    features: ['Hand-crafted', 'Problem-solving', 'Benchmark quality']
  },
  {
    id: 'mbpp',
    name: 'MBPP',
    description: '974 Mostly Basic Python Problems',
    size: '974',
    recommended: false,
    icon: '🐍',
    features: ['Basic to intermediate', 'Diverse domains', 'Test cases included']
  }
];

export default function FinetuningPage() {
  const { models } = useModels();
  const [step, setStep] = useState<Step>('select-model');
  const [selectedModel, setSelectedModel] = useState<any>(null);
  const [evaluations, setEvaluations] = useState<any[]>([]);
  const [selectedEvaluation, setSelectedEvaluation] = useState<any>(null);
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [trainingFile, setTrainingFile] = useState<string | null>(null);
  const [finetuningJob, setFinetuningJob] = useState<any>(null);
  const [newModelName, setNewModelName] = useState('');
  const [selectedDataset, setSelectedDataset] = useState('code_alpaca');

  // Load evaluations from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('evaluations');
    if (saved) {
      setEvaluations(JSON.parse(saved));
    }
  }, []);

  // Filter evaluations for selected model
  const modelEvaluations = evaluations.filter(e => 
    e.models?.includes(selectedModel?.model_id) && e.status === 'completed'
  );

  // Generate new model name
  useEffect(() => {
    if (selectedModel) {
      const baseName = selectedModel.model_id.split(':')[0];
      const timestamp = new Date().toISOString().slice(0, 10).replace(/-/g, '');
      setNewModelName(`${baseName}-finetuned-${timestamp}`);
    }
  }, [selectedModel]);

  const analyzeEvaluation = async () => {
    if (!selectedEvaluation) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await finetuningApi.analyze(selectedEvaluation.evaluation_id);
      setAnalysis(response.analysis);
      setStep('analyze');
    } catch (err) {
      setError('Failed to analyze evaluation');
    } finally {
      setLoading(false);
    }
  };

  const prepareData = async () => {
    if (!selectedEvaluation) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await finetuningApi.prepareTrainingData({
        evaluation_id: selectedEvaluation.evaluation_id,
        dataset_id: selectedDataset,
        max_problems: 100
      });
      
      if (response.success) {
        setTrainingFile(response.training_file);
        setStep('train');
      }
    } catch (err) {
      setError('Failed to prepare training data');
    } finally {
      setLoading(false);
    }
  };

  const startFinetuning = async () => {
    if (!trainingFile || !selectedModel) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await finetuningApi.startFinetuning({
        base_model: selectedModel.model_id,
        training_file: trainingFile,
        output_model: newModelName
      });
      
      setFinetuningJob(response);
      setStep('complete');
    } catch (err) {
      setError('Failed to start fine-tuning');
    } finally {
      setLoading(false);
    }
  };

  const resetFlow = () => {
    setStep('select-model');
    setSelectedModel(null);
    setSelectedEvaluation(null);
    setAnalysis(null);
    setTrainingFile(null);
    setFinetuningJob(null);
    setError(null);
  };

  const getDatasetInfo = (datasetId: string) => {
    return DATASETS.find(d => d.id === datasetId) || DATASETS[0];
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">🎯 Model Fine-tuning Studio</h1>
        <p className="text-gray-600 mt-1">
          Improve your models by fine-tuning them based on evaluation results
        </p>
      </div>

      {/* Progress Steps */}
      <div className="mb-8">
        <div className="flex items-center">
          {[
            { id: 'select-model', label: 'Select Model', icon: '🤖' },
            { id: 'select-evaluation', label: 'Select Evaluation', icon: '📋' },
            { id: 'analyze', label: 'Analyze', icon: '📊' },
            { id: 'prepare', label: 'Prepare Data', icon: '🔧' },
            { id: 'train', label: 'Train', icon: '🚀' },
            { id: 'complete', label: 'Complete', icon: '✅' },
          ].map((s, i) => {
            const stepIndex = ['select-model', 'select-evaluation', 'analyze', 'prepare', 'train', 'complete'].indexOf(step);
            const isActive = step === s.id;
            const isComplete = ['select-model', 'select-evaluation', 'analyze', 'prepare', 'train', 'complete'].indexOf(s.id) <= stepIndex;
            
            return (
              <div key={s.id} className="flex items-center flex-1">
                <div className={`flex items-center justify-center w-8 h-8 rounded-full text-sm ${
                  isActive ? 'bg-blue-600 text-white' :
                  isComplete ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-600'
                }`}>
                  {isComplete && s.id !== step ? '✓' : s.icon}
                </div>
                <div className={`ml-2 text-xs font-medium hidden sm:block ${
                  isActive ? 'text-blue-600' : isComplete ? 'text-green-600' : 'text-gray-500'
                }`}>
                  {s.label}
                </div>
                {i < 5 && (
                  <div className={`flex-1 h-0.5 mx-2 ${
                    isComplete ? 'bg-green-500' : 'bg-gray-200'
                  }`} />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {loading && <LoadingSpinner />}

      {/* Step 1: Select Model */}
      {step === 'select-model' && (
        <Card>
          <h2 className="text-xl font-semibold mb-6">🤖 Step 1: Select Model to Fine-tune</h2>
          
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {models.filter(m => m.active).map(model => (
                <button
                  key={model.model_id}
                  onClick={() => {
                    setSelectedModel(model);
                    setStep('select-evaluation');
                  }}
                  className={`p-6 border-2 rounded-lg text-left transition-all hover:shadow-md ${
                    selectedModel?.model_id === model.model_id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-blue-300'
                  }`}
                >
                  <p className="font-semibold text-lg">{model.model_id}</p>
                  <p className="text-sm text-gray-500 mt-1">{model.provider}</p>
                  <span className="inline-block mt-3 text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                    Active
                  </span>
                </button>
              ))}
            </div>

            {models.filter(m => m.active).length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <p className="mb-4">No active models available</p>
                <Link href="/models" className="text-blue-600 hover:underline">
                  Go to Models page
                </Link>
              </div>
            )}
          </div>
        </Card>
      )}

      {/* Step 2: Select Evaluation */}
      {step === 'select-evaluation' && selectedModel && (
        <Card>
          <h2 className="text-xl font-semibold mb-6">📋 Step 2: Select Evaluation for {selectedModel.model_id}</h2>
          
          <div className="space-y-6">
            {modelEvaluations.length > 0 ? (
              <div className="space-y-3">
                {modelEvaluations.map(evalItem => (
                  <button
                    key={evalItem.evaluation_id}
                    onClick={() => setSelectedEvaluation(evalItem)}
                    className={`w-full p-4 border rounded-lg text-left transition-colors ${
                      selectedEvaluation?.evaluation_id === evalItem.evaluation_id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-blue-300'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-medium">{evalItem.evaluation_id}</p>
                        <p className="text-sm text-gray-500">
                          {new Date(evalItem.created_at).toLocaleString()}
                        </p>
                      </div>
                      <div className="flex items-center space-x-3">
                        <span className="text-sm text-gray-500">
                          Progress: {evalItem.progress}%
                        </span>
                        {selectedEvaluation?.evaluation_id === evalItem.evaluation_id && (
                          <span className="text-blue-600">✓ Selected</span>
                        )}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 bg-gray-50 rounded-lg">
                <p className="text-gray-500 mb-4">No completed evaluations found for {selectedModel.model_id}</p>
                <Link 
                  href="/evaluations/new" 
                  className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Create New Evaluation
                </Link>
              </div>
            )}

            {/* Navigation */}
            <div className="flex justify-between pt-4 border-t">
              <button
                onClick={() => setStep('select-model')}
                className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                ← Back to Models
              </button>
              {modelEvaluations.length > 0 && (
                <button
                  onClick={analyzeEvaluation}
                  disabled={!selectedEvaluation || loading}
                  className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
                >
                  Continue to Analysis →
                </button>
              )}
            </div>
          </div>
        </Card>
      )}

      {/* Step 3: Analysis Results */}
      {step === 'analyze' && analysis && selectedEvaluation && (
        <Card>
          <h2 className="text-xl font-semibold mb-6">📊 Step 3: Analysis Results</h2>
          
          <div className="space-y-6">
            {/* Evaluation Info */}
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600">Analyzing evaluation:</p>
              <p className="font-medium">{selectedEvaluation.evaluation_id}</p>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg text-center">
                <p className="text-2xl font-bold text-blue-600">{analysis.total_problems}</p>
                <p className="text-sm text-gray-600">Total Problems</p>
              </div>
              <div className="bg-red-50 p-4 rounded-lg text-center">
                <p className="text-2xl font-bold text-red-600">{analysis.total_failures}</p>
                <p className="text-sm text-gray-600">Failed</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg text-center">
                <p className="text-2xl font-bold text-purple-600">
                  {(analysis.failure_rate * 100).toFixed(1)}%
                </p>
                <p className="text-sm text-gray-600">Failure Rate</p>
              </div>
            </div>

            {/* Error Breakdown */}
            <div>
              <h3 className="font-semibold mb-3">Error Types</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {Object.entries(analysis.error_analysis?.by_type || {}).map(([type, count]) => (
                  <div key={type} className="bg-gray-50 p-3 rounded-lg">
                    <p className="text-lg font-bold text-gray-800">{String(count)}</p>
                    <p className="text-xs text-gray-600">{type.replace(/_/g, ' ')}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Recommendations */}
            {analysis.recommendations.length > 0 && (
              <div className="bg-yellow-50 p-4 rounded-lg">
                <h3 className="font-semibold mb-2">💡 Recommendations</h3>
                <ul className="space-y-1">
                  {analysis.recommendations.map((rec: string, i: number) => (
                    <li key={i} className="text-sm flex items-start">
                      <span className="text-yellow-600 mr-2">•</span>
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Navigation */}
            <div className="flex justify-between pt-4 border-t">
              <button
                onClick={() => setStep('select-evaluation')}
                className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                ← Back
              </button>
              <button
                onClick={() => setStep('prepare')}
                className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Continue to Data Preparation →
              </button>
            </div>
          </div>
        </Card>
      )}

      {/* Step 4: Data Preparation - WITH CLEAR DATASET INFORMATION */}
      {step === 'prepare' && (
        <Card>
          <h2 className="text-xl font-semibold mb-6">🔧 Step 4: Prepare Training Data</h2>
          
          <div className="space-y-6">
            {/* Dataset Selection - Clearly Visible */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Select Training Dataset
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {DATASETS.map(dataset => {
                  const isSelected = selectedDataset === dataset.id;
                  return (
                    <button
                      key={dataset.id}
                      onClick={() => setSelectedDataset(dataset.id)}
                      className={`p-4 border-2 rounded-lg text-left transition-all ${
                        isSelected
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-blue-300'
                      }`}
                    >
                      <div className="flex items-start">
                        <span className="text-2xl mr-3">{dataset.icon}</span>
                        <div className="flex-1">
                          <div className="flex items-center">
                            <p className="font-semibold">{dataset.name}</p>
                            {dataset.recommended && (
                              <span className="ml-2 text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded">
                                Recommended
                              </span>
                            )}
                          </div>
                          <p className="text-sm text-gray-600 mt-1">{dataset.description}</p>
                          <div className="mt-2 flex flex-wrap gap-2">
                            {dataset.features.map((feature, i) => (
                              <span key={i} className="text-xs bg-gray-100 text-gray-700 px-2 py-0.5 rounded">
                                {feature}
                              </span>
                            ))}
                          </div>
                          <p className="text-xs text-gray-400 mt-2">Size: {dataset.size} examples</p>
                        </div>
                        {isSelected && (
                          <span className="text-blue-600 text-xl ml-2">✓</span>
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Selected Dataset Info */}
            <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
              <div className="flex items-start">
                <span className="text-2xl mr-3">{getDatasetInfo(selectedDataset).icon}</span>
                <div>
                  <h3 className="font-semibold text-blue-800">
                    Using {getDatasetInfo(selectedDataset).name} Dataset
                  </h3>
                  <p className="text-sm text-blue-700 mt-1">
                    {getDatasetInfo(selectedDataset).description}
                  </p>
                </div>
              </div>
            </div>

            {/* What will be created */}
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-medium mb-2">Training Data Overview:</h3>
              <ul className="space-y-2 text-sm">
                <li className="flex justify-between">
                  <span>Failure examples from your evaluation:</span>
                  <span className="font-medium">{analysis?.total_failures || 0}</span>
                </li>
                <li className="flex justify-between">
                  <span>Similar problems from {getDatasetInfo(selectedDataset).name}:</span>
                  <span className="font-medium">100</span>
                </li>
                <li className="flex justify-between pt-2 border-t">
                  <span>Total training examples:</span>
                  <span className="font-bold">{(analysis?.total_failures || 0) + 100}</span>
                </li>
              </ul>
            </div>

            {/* Navigation */}
            <div className="flex justify-between pt-4 border-t">
              <button
                onClick={() => setStep('analyze')}
                className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                ← Back
              </button>
              <button
                onClick={prepareData}
                disabled={loading}
                className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-400"
              >
                {loading ? 'Preparing...' : 'Generate Training Data →'}
              </button>
            </div>
          </div>
        </Card>
      )}

      {/* Step 5: Training */}
      {step === 'train' && trainingFile && (
        <Card>
          <h2 className="text-xl font-semibold mb-6">🚀 Step 5: Start Fine-tuning</h2>
          
          <div className="space-y-6">
            {/* Training Configuration */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Base Model</p>
                <p className="font-mono font-medium">{selectedModel?.model_id}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  New Model Name
                </label>
                <input
                  type="text"
                  value={newModelName}
                  onChange={(e) => setNewModelName(e.target.value)}
                  className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono"
                />
                <p className="text-xs text-gray-500 mt-1">
                  This model will be available after fine-tuning with a "Fine-tuned" badge
                </p>
              </div>
            </div>

            {/* Dataset Summary */}
            <div className="bg-blue-50 p-3 rounded-lg">
              <p className="text-sm text-blue-800">
                <span className="font-medium">Dataset:</span> {getDatasetInfo(selectedDataset).name} ({getDatasetInfo(selectedDataset).size} examples)
              </p>
            </div>

            {/* Training Data Ready */}
            <div className="bg-green-50 p-4 rounded-lg">
              <p className="text-sm text-green-800">
                ✅ Training data prepared successfully
              </p>
            </div>

            {/* Time Estimate */}
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-sm text-blue-800">
                ⏱️ Fine-tuning typically takes 10-30 minutes. You can check status in the Models page.
              </p>
            </div>

            {/* Navigation */}
            <div className="flex justify-between pt-4 border-t">
              <button
                onClick={() => setStep('prepare')}
                className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                ← Back
              </button>
              <button
                onClick={startFinetuning}
                disabled={loading}
                className="px-6 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:bg-gray-400"
              >
                {loading ? 'Starting...' : '🚀 Start Fine-tuning'}
              </button>
            </div>
          </div>
        </Card>
      )}

      {/* Step 6: Complete */}
      {step === 'complete' && finetuningJob && (
        <Card>
          <div className="text-center py-8">
            {finetuningJob.success ? (
              <>
                <div className="text-6xl mb-4">🎉</div>
                <h2 className="text-2xl font-bold text-green-600 mb-4">
                  Fine-tuning Started Successfully!
                </h2>
                <p className="text-gray-600 mb-2">
                  Your new model is being created:
                </p>
                <p className="font-mono bg-gray-100 px-4 py-2 rounded inline-block mb-6">
                  {newModelName}
                </p>
                
                {/* Next Steps */}
                <div className="max-w-md mx-auto bg-blue-50 p-6 rounded-lg mb-6">
                  <h3 className="font-medium mb-3">📋 What happens next?</h3>
                  <ul className="text-left space-y-3 text-sm">
                    <li className="flex items-start">
                      <span className="text-blue-600 mr-2">1.</span>
                      <span>Fine-tuning runs in background (10-30 minutes)</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-blue-600 mr-2">2.</span>
                      <span>When complete, model appears in Models list with <span className="bg-purple-100 text-purple-800 px-2 py-0.5 rounded text-xs ml-1">Fine-tuned</span> badge</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-blue-600 mr-2">3.</span>
                      <span>Use it in new evaluations and compare performance</span>
                    </li>
                  </ul>
                </div>

                {/* Action Buttons */}
                <div className="flex justify-center space-x-4">
                  <Link
                    href="/models"
                    className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  >
                    View Models
                  </Link>
                  <button
                    onClick={resetFlow}
                    className="px-6 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
                  >
                    Start New Fine-tuning
                  </button>
                </div>
              </>
            ) : (
              <>
                <div className="text-6xl mb-4">❌</div>
                <h2 className="text-2xl font-bold text-red-600 mb-4">
                  Fine-tuning Failed
                </h2>
                <p className="text-gray-600 mb-6">{finetuningJob.error}</p>
                <button
                  onClick={() => setStep('train')}
                  className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Try Again
                </button>
              </>
            )}
          </div>
        </Card>
      )}
    </div>
  );
}