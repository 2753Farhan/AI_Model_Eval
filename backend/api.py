# backend/api.py
"""
Flask API for AI Model Evaluation
Run: python api.py
"""

import os
import sys
import asyncio
import json
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add src to path
sys.path.append(str(Path(__file__).parent))

# Create Flask app
app = Flask(__name__)

# Configure CORS for frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Import your modules
from src.entities import Evaluation, EvaluationResult
from src.managers import EvaluationManager, ResultAggregator
from src.adapters import ModelRegistry
from src.loaders import HumanEvalLoader
from src.executors import SandboxExecutor
from src.calculators import (
    FunctionalMetricsCalculator,
    QualityMetricsCalculator,
    SemanticMetricsCalculator
)
from src.analyzers import ErrorAnalyzer
from src.generators import ReportGenerator
from src.config.config_manager import ConfigManager
from src.entities import EvaluationResult
from src.finetuning.analyzer import FailureAnalyzer
from src.finetuning.dataset_preparer import DatasetPreparer
from src.finetuning.trainer import OllamaTrainer
from src.loaders import DatasetLoader

# Initialize fine-tuning components
failure_analyzer = FailureAnalyzer()
dataset_preparer = DatasetPreparer()
ollama_trainer = OllamaTrainer()


# Initialize components
config = ConfigManager("config/settings.yaml")
model_registry = ModelRegistry()
model_registry.load_from_config(config.config)

dataset_loader = HumanEvalLoader({
    'repo_url': config.get('paths.repo_url'),
    'data_dir': config.get('paths.data_dir'),
    'name': 'HumanEval'
})

sandbox = SandboxExecutor(
    timeout=config.get('evaluation.timeout_seconds', 30),
    memory_limit=f"{config.get('evaluation.max_memory_mb', 512)}m"
)

metric_calculator = FunctionalMetricsCalculator()
quality_calculator = QualityMetricsCalculator({})
semantic_calculator = SemanticMetricsCalculator({})

error_analyzer = ErrorAnalyzer()
evaluation_manager = EvaluationManager(
    model_registry=model_registry,
    dataset_loader=dataset_loader,
    sandbox_executor=sandbox,
    metric_calculator=metric_calculator,
    error_analyzer=error_analyzer
)

result_aggregator = ResultAggregator()

# Create event loop for async operations
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)



def run_async(coro):
    """Run async coroutine in thread"""
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    return future.result(timeout=300)

# Start loop in background thread
def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=start_loop, daemon=True).start()

# Store active evaluations
active_evaluations = {}


@app.route('/api/finetuning/analyze/<evaluation_id>', methods=['GET', 'OPTIONS'])
def analyze_for_finetuning(evaluation_id):
    """Analyze evaluation results for fine-tuning opportunities"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Get evaluation results
        results = evaluation_manager.get_results(evaluation_id)
        
        if not results:
            return jsonify({'error': 'No results found'}), 404
        
        # Analyze failures
        analysis = failure_analyzer.analyze_evaluation(results)
        
        return jsonify({
            'success': True,
            'evaluation_id': evaluation_id,
            'analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/finetuning/datasets', methods=['GET', 'OPTIONS'])
def list_finetuning_datasets():
    """List available datasets for fine-tuning"""
    if request.method == 'OPTIONS':
        return '', 204
    
    # You can add more datasets here
    datasets = [
        {
            'id': 'code_alpaca',
            'name': 'Code Alpaca',
            'description': '20k instruction-following examples for code generation',
            'size': 20000,
            'format': 'jsonl'
        },
        {
            'id': 'python_codesearchnet',
            'name': 'CodeSearchNet Python',
            'description': 'Python code from GitHub with docstrings',
            'size': 50000,
            'format': 'jsonl'
        }
    ]
    
    return jsonify(datasets)

@app.route('/api/finetuning/prepare', methods=['POST', 'OPTIONS'])
def prepare_training_data():
    """Prepare training data based on failures"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        evaluation_id = data.get('evaluation_id')
        dataset_id = data.get('dataset_id', 'code_alpaca')
        max_problems = data.get('max_problems', 100)
        
        # Get evaluation results
        results = evaluation_manager.get_results(evaluation_id)
        failures = [r for r in results if not r.passed]
        
        if not failures:
            return jsonify({'error': 'No failures found'}), 400
        
        # Load candidate dataset
        # This is a placeholder - you'd need to implement actual dataset loading
        candidate_dataset = DatasetLoader({
            'name': dataset_id,
            'path': f'data/datasets/{dataset_id}.jsonl'
        })
        
        # For now, create a mock dataset
        class MockDataset:
            def __init__(self):
                self.problems = []
        
        candidate_dataset = MockDataset()
        
        # Find similar problems
        similar_problems = dataset_preparer.find_similar_problems(
            failures, candidate_dataset, max_problems
        )
        
        # Create training data
        training_file = dataset_preparer.create_training_data(
            failures, similar_problems,
            f"training_{evaluation_id}.jsonl"
        )
        
        return jsonify({
            'success': True,
            'training_file': training_file,
            'failure_count': len(failures),
            'similar_problems': len(similar_problems)
        })
        
    except Exception as e:
        logger.error(f"Preparation failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/finetuning/train', methods=['POST', 'OPTIONS'])
def start_finetuning():
    """Start fine-tuning a model"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        base_model = data.get('base_model', 'codellama:7b')
        training_file = data.get('training_file')
        output_model = data.get('output_model', f"{base_model}-finetuned")
        
        if not training_file:
            return jsonify({'error': 'Training file required'}), 400
        
        # Start fine-tuning
        result = ollama_trainer.fine_tune(
            base_model=base_model,
            training_file=training_file,
            output_model=output_model,
            wait_for_completion=False  # Don't wait, it's long-running
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Fine-tuning failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/finetuning/models', methods=['GET', 'OPTIONS'])
def list_finetuned_models():
    """List fine-tuned models"""
    if request.method == 'OPTIONS':
        return '', 204
    
    models = ollama_trainer.list_finetuned_models()
    return jsonify(models)

@app.route('/api/finetuning/status/<job_id>', methods=['GET', 'OPTIONS'])
def finetuning_status(job_id):
    """Check fine-tuning job status"""
    if request.method == 'OPTIONS':
        return '', 204
    
    # This would need a job tracking system
    # For now, return mock status
    return jsonify({
        'job_id': job_id,
        'status': 'running',
        'progress': 45,
        'eta': '5 minutes'
    })


@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health():
    if request.method == 'OPTIONS':
        return '', 204
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

# In your backend/api.py, replace the list_models endpoint

@app.route('/api/models', methods=['GET', 'OPTIONS'])
def list_models():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Get all registered models from your registry
        registered_models = model_registry.list_models()
        
        # Check which models are actually running in Ollama
        active_models = get_active_ollama_models()
        
        # Update active status
        for model in registered_models:
            model['active'] = model['model_id'] in active_models
        
        return jsonify(registered_models)
    except Exception as e:
        print(f"Error listing models: {e}")
        return jsonify([])

def get_active_ollama_models():
    """Check which models are currently running in Ollama"""
    import subprocess
    import json
    
    try:
        # Run ollama ps command to get running models
        result = subprocess.run(
            ['ollama', 'ps'], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        if result.returncode != 0:
            print(f"Ollama ps failed: {result.stderr}")
            return []
        
        # Parse the output
        lines = result.stdout.strip().split('\n')
        if len(lines) < 2:  # No running models
            return []
        
        # Skip header line, extract model names
        active_models = []
        for line in lines[1:]:
            if line.strip():
                # Format: NAME ID SIZE PROCESSOR UNTIL
                parts = line.split()
                if parts:
                    model_name = parts[0]
                    active_models.append(model_name)
        
        return active_models
        
    except FileNotFoundError:
        print("Ollama not found in PATH")
        return []
    except Exception as e:
        print(f"Error checking active models: {e}")
        return []

# Alternative: Use Ollama API instead of subprocess
def get_active_models_via_api():
    """Use Ollama API to check running models"""
    import requests
    
    try:
        response = requests.get(
            'http://localhost:11434/api/ps',
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            # Extract model names from response
            models = data.get('models', [])
            return [m['name'] for m in models]
        return []
    except:
        return []

@app.route('/api/datasets', methods=['GET'])
def list_datasets():
    """List available datasets"""
    try:
        problems = dataset_loader.load_dataset()
        return jsonify([{
            'id': 'humaneval',
            'name': 'HumanEval',
            'problems': len(problems),
            'description': 'OpenAI HumanEval dataset for code generation'
        }])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/datasets/<dataset_id>/samples', methods=['GET'])
def get_dataset_samples(dataset_id):
    """Get samples for a specific dataset"""
    try:
        limit = int(request.args.get('limit', 164))
        offset = int(request.args.get('offset', 0))
        
        # Ensure dataset is loaded
        if not getattr(dataset_loader, 'problems', None):
            dataset_loader.load_dataset()
            
        problems = dataset_loader.problems
        
        # Paginate
        start_idx = offset
        end_idx = min(offset + limit, len(problems))
        paginated = problems[start_idx:end_idx]
        
        # Format for frontend
        samples = []
        for p in paginated:
            # Estimate difficulty based on problem stats or index if not available
            difficulty = "Easy"
            if p.stats:
                comp = p.stats.get('cyclomatic_complexity', 0)
                if comp > 7:
                    difficulty = "Hard"
                elif comp > 3:
                    difficulty = "Medium"
                    
            samples.append({
                'task_id': p.task_id,
                'prompt': p.prompt,
                'canonical_solution': p.canonical_solution,
                'test': p.test_cases,
                'entry_point': p.entry_point,
                'difficulty': difficulty,
                'tags': p.metadata.get('tags', ['python', 'eval'])
            })
            
        return jsonify({
            'samples': samples,
            'total': len(problems)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/metrics/code', methods=['POST', 'OPTIONS'])
def analyze_code_metrics():
    """Calculate various metrics for a code block using existing calculators"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Create a temporary evaluation result to use with calculators
        temp_result = EvaluationResult(
            evaluation_id='temp',
            problem_id='temp',
            model_id='temp',
            sample_id=0
        )
        temp_result.set_generated_code(code)
        
        # Calculate metrics using existing calculators
        metrics = {}
        
        # Quality metrics (cyclomatic complexity, maintainability, etc.)
        quality_metrics = quality_calculator.calculate_per_file(code)
        metrics.update(quality_metrics)
        
        # Add quality grade
        metrics['quality_grade'] = quality_calculator.grade_quality(quality_metrics)
        
        # Basic metrics
        lines = code.split('\n')
        metrics['loc'] = len(lines)
        metrics['blank_lines'] = sum(1 for line in lines if line.strip() == '')
        metrics['code_lines'] = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
        metrics['comment_lines'] = sum(1 for line in lines if line.strip().startswith('#'))
        
        # Function count (simple approximation)
        metrics['function_count'] = code.count('def ')
        
        # Class count
        metrics['class_count'] = code.count('class ')
        
        # Import count
        metrics['import_count'] = code.count('import ') + code.count('from ')
        
        # Calculate semantic metrics if there's reference code
        if 'reference' in data:
            semantic_metrics = semantic_calculator._calculate_codebleu(
                code, 
                data['reference']
            )
            metrics['codebleu'] = semantic_metrics
        
        return jsonify({
            'success': True,
            'language': language,
            'metrics': metrics,
            'summary': generate_metrics_summary(metrics)
        })
        
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/metrics/compare', methods=['POST', 'OPTIONS'])
def compare_code_metrics():
    """Compare metrics between two code blocks using existing calculators"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        code1 = data.get('code1', '')
        code2 = data.get('code2', '')
        language = data.get('language', 'python')
        
        if not code1 or not code2:
            return jsonify({'error': 'Both code blocks required'}), 400
        
        # Calculate metrics for both using helper
        metrics1 = calculate_code_metrics_helper(code1)
        metrics2 = calculate_code_metrics_helper(code2)
        
        # Calculate similarity safely
        similarity = None
        if data.get('calculate_similarity', False):
            try:
                # The _calculate_codebleu method returns a float, not a list
                similarity = semantic_calculator._calculate_codebleu(code1, code2)
                # Ensure it's a float
                if similarity is not None:
                    similarity = float(similarity)
            except Exception as e:
                print(f"Error calculating similarity: {e}")
                similarity = None
        
        # Calculate differences safely
        differences = {}
        all_keys = set(metrics1.keys()) | set(metrics2.keys())
        for key in all_keys:
            val1 = metrics1.get(key, 0)
            val2 = metrics2.get(key, 0)
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                differences[key] = val2 - val1
        
        # Determine which is better based on multiple factors
        better = 'equal'
        reason = 'Similar metrics'
        
        # Weighted scoring system
        score1 = 0
        score2 = 0
        
        # Maintainability index (higher is better)
        mi1 = metrics1.get('maintainability_index', 0)
        mi2 = metrics2.get('maintainability_index', 0)
        if mi1 > mi2:
            score1 += 2
        elif mi2 > mi1:
            score2 += 2
        
        # Cyclomatic complexity (lower is better)
        cc1 = metrics1.get('cyclomatic_complexity', 0)
        cc2 = metrics2.get('cyclomatic_complexity', 0)
        if cc1 < cc2:
            score1 += 1
        elif cc2 < cc1:
            score2 += 1
        
        # Lines of code (fewer is generally better)
        loc1 = metrics1.get('loc', 0)
        loc2 = metrics2.get('loc', 0)
        if loc1 < loc2:
            score1 += 1
        elif loc2 < loc1:
            score2 += 1
        
        if score1 > score2:
            better = 'code1'
            reason = 'Better overall metrics'
        elif score2 > score1:
            better = 'code2'
            reason = 'Better overall metrics'
        
        # Prepare response
        comparison = {
            'code1': metrics1,
            'code2': metrics2,
            'similarity': similarity,
            'differences': differences,
            'better': better,
            'reason': reason,
            'scores': {
                'code1': score1,
                'code2': score2
            }
        }
        
        return jsonify({
            'success': True,
            'comparison': comparison
        })
        
    except Exception as e:
        print(f"Error comparing metrics: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'success': False}), 500


def calculate_code_metrics_helper(code: str) -> dict:
    """Helper to calculate metrics for a code block safely"""
    metrics = {}
    
    try:
        # Use quality calculator
        quality_metrics = quality_calculator.calculate_per_file(code)
        if quality_metrics:
            metrics.update(quality_metrics)
        
        # Add quality grade
        try:
            metrics['quality_grade'] = quality_calculator.grade_quality(quality_metrics)
        except:
            metrics['quality_grade'] = 'Unknown'
        
        # Basic metrics
        lines = code.split('\n')
        metrics['total_lines'] = len(lines)
        metrics['blank_lines'] = sum(1 for line in lines if line.strip() == '')
        metrics['code_lines'] = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
        metrics['comment_lines'] = sum(1 for line in lines if line.strip().startswith('#'))
        
        # Count functions, classes, imports (safely)
        metrics['function_count'] = code.count('def ')
        metrics['class_count'] = code.count('class ')
        metrics['import_count'] = code.count('import ') + code.count('from ')
        
        # Ensure all numeric values are proper floats
        for key, value in metrics.items():
            if isinstance(value, (int, float)) and not isinstance(value, float):
                metrics[key] = float(value)
        
    except Exception as e:
        print(f"Error in metrics helper: {e}")
        metrics['error'] = str(e)
    
    return metrics

def generate_metrics_summary(metrics: dict) -> str:
    """Generate a human-readable summary of metrics"""
    summary = []
    
    if metrics.get('quality_grade'):
        summary.append(f"Quality Grade: {metrics['quality_grade']}")
    
    if metrics.get('maintainability_index'):
        mi = metrics['maintainability_index']
        if mi >= 80:
            summary.append("Maintainability: Excellent")
        elif mi >= 60:
            summary.append("Maintainability: Good")
        elif mi >= 40:
            summary.append("Maintainability: Fair")
        else:
            summary.append("Maintainability: Poor")
    
    if metrics.get('cyclomatic_complexity'):
        cc = metrics['cyclomatic_complexity']
        if cc <= 5:
            summary.append("Complexity: Low")
        elif cc <= 10:
            summary.append("Complexity: Moderate")
        else:
            summary.append("Complexity: High")
    
    if metrics.get('loc'):
        summary.append(f"Lines of Code: {metrics['loc']}")
    
    if metrics.get('function_count'):
        summary.append(f"Functions: {metrics['function_count']}")
    
    if metrics.get('class_count'):
        summary.append(f"Classes: {metrics['class_count']}")
    
    return " | ".join(summary) if summary else "Metrics calculated"


@app.route('/api/metrics/batch', methods=['POST', 'OPTIONS'])
def batch_metrics():
    """Calculate metrics for multiple code blocks"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        codes = data.get('codes', [])
        
        if not codes:
            return jsonify({'error': 'No codes provided'}), 400
        
        results = []
        for i, code in enumerate(codes):
            metrics = calculate_code_metrics_helper(code)
            results.append({
                'index': i,
                'metrics': metrics,
                'summary': generate_metrics_summary(metrics)
            })
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/metrics/explain/<metric_name>', methods=['GET', 'OPTIONS'])
def explain_metric(metric_name):
    """Get explanation for a specific metric"""
    if request.method == 'OPTIONS':
        return '', 204
    
    explanations = {
        'cyclomatic_complexity': {
            'name': 'Cyclomatic Complexity',
            'description': 'Measures the number of linearly independent paths through code. Lower is better.',
            'range': '0-20+',
            'thresholds': {
                'good': '≤ 5',
                'moderate': '6-10',
                'high': '≥ 11'
            },
            'formula': 'M = E - N + 2P (where E = edges, N = nodes, P = connected components)'
        },
        'maintainability_index': {
            'name': 'Maintainability Index',
            'description': 'Measures how maintainable the code is. Higher is better.',
            'range': '0-100',
            'thresholds': {
                'excellent': '≥ 80',
                'good': '60-79',
                'fair': '40-59',
                'poor': '< 40'
            },
            'formula': 'MI = 171 - 5.2 * ln(meanV) - 0.23 * meanG - 16.2 * ln(meanLOC)'
        },
        'cognitive_complexity': {
            'name': 'Cognitive Complexity',
            'description': 'Measures how difficult code is to understand. Lower is better.',
            'range': '0-50+',
            'thresholds': {
                'low': '≤ 5',
                'moderate': '6-15',
                'high': '≥ 16'
            }
        },
        'loc': {
            'name': 'Lines of Code',
            'description': 'Total number of lines in the code file.',
            'range': 'Varies',
            'thresholds': {}
        },
        'codebleu': {
            'name': 'CodeBLEU',
            'description': 'Semantic similarity score between code snippets. Higher is better.',
            'range': '0-1',
            'thresholds': {
                'good': '≥ 0.8',
                'moderate': '0.5-0.79',
                'poor': '< 0.5'
            }
        }
    }
    
    if metric_name in explanations:
        return jsonify(explanations[metric_name])
    else:
        return jsonify({
            'name': metric_name.replace('_', ' ').title(),
            'description': f'Metric: {metric_name}',
            'range': 'Unknown',
            'thresholds': {}
        })

@app.route('/api/evaluations', methods=['GET'])
def get_evaluations():
    """Get all evaluations"""
    try:
        evaluations = []
        for eval_id, eval_obj in evaluation_manager.evaluations.items():
            eval_dict = eval_obj.to_dict() if hasattr(eval_obj, 'to_dict') else {}
            eval_dict['results_count'] = len(eval_obj.results_ids)
            evaluations.append(eval_dict)
        return jsonify(evaluations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluations', methods=['POST'])
def create_evaluation():
    """Create a new evaluation"""
    try:
        data = request.json
        evaluation = evaluation_manager.create_evaluation(
            user_id=data.get('user_id', 'api_user'),
            model_ids=data.get('models', []),
            dataset_id=data.get('dataset_id', 'humaneval'),
            config=data.get('config', {})
        )
        active_evaluations[evaluation.evaluation_id] = evaluation
        return jsonify({
            'evaluation_id': evaluation.evaluation_id,
            'status': 'created'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluations/<evaluation_id>/start', methods=['POST'])
def start_evaluation(evaluation_id):
    """Start an evaluation"""
    try:
        if evaluation_id not in active_evaluations:
            return jsonify({'error': 'Evaluation not found'}), 404
        
        # Run evaluation in background
        async def run_evaluation_task():
            try:
                evaluation = await evaluation_manager.run_evaluation(evaluation_id)
                results = evaluation_manager.get_results(evaluation_id)
                result_aggregator.add_results(evaluation_id, results)
                
                active_evaluations[evaluation_id] = {
                    'evaluation': evaluation,
                    'results': results,
                    'status': 'completed'
                }
                return evaluation
            except Exception as e:
                active_evaluations[evaluation_id] = {
                    'error': str(e),
                    'status': 'failed'
                }
                return None
        
        # Submit task to event loop
        future = asyncio.run_coroutine_threadsafe(run_evaluation_task(), loop)
        
        return jsonify({'status': 'started'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluations/<evaluation_id>/status', methods=['GET'])
def evaluation_status(evaluation_id):
    """Get evaluation status"""
    try:
        # Check stored results
        if evaluation_id in active_evaluations:
            eval_data = active_evaluations[evaluation_id]
            if isinstance(eval_data, dict) and eval_data.get('status') == 'completed':
                return jsonify({
                    'evaluation_id': evaluation_id,
                    'status': 'completed',
                    'progress': 100,
                    'current_stage': 'completed'
                })
            elif isinstance(eval_data, dict) and eval_data.get('status') == 'failed':
                return jsonify({
                    'evaluation_id': evaluation_id,
                    'status': 'failed',
                    'error': eval_data.get('error', 'Unknown error')
                })
        
        # Get from manager
        evaluation = evaluation_manager.get_evaluation(evaluation_id)
        if not evaluation:
            return jsonify({'error': 'Evaluation not found'}), 404
        
        return jsonify({
            'evaluation_id': evaluation.evaluation_id,
            'status': evaluation.status.value,
            'progress': evaluation.progress,
            'current_stage': evaluation.current_stage
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluations/<evaluation_id>/results', methods=['GET'])
def get_results(evaluation_id):
    """Get evaluation results"""
    try:
        # Check stored results
        if evaluation_id in active_evaluations:
            eval_data = active_evaluations[evaluation_id]
            if isinstance(eval_data, dict) and 'results' in eval_data:
                return jsonify([r.to_dict() for r in eval_data['results']])
        
        # Get from manager
        results = evaluation_manager.get_results(evaluation_id)
        return jsonify([r.to_dict() for r in results])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluations/<evaluation_id>/cancel', methods=['POST'])
def cancel_evaluation(evaluation_id):
    """Cancel an evaluation"""
    try:
        success = evaluation_manager.cancel_evaluation(evaluation_id)
        if success:
            return jsonify({'status': 'cancelled'})
        return jsonify({'error': 'Failed to cancel'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """Analyze code with sandbox"""
    try:
        data = request.json
        code = data.get('code', '')
        test_cases = data.get('test_cases', [])
        
        async def analyze():
            return await sandbox.execute_safely(
                code=code,
                test_cases=test_cases,
                problem_id='api_analysis',
                language='python'
            )
        
        result = run_async(analyze())
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'passed': False}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        stats = {
            'evaluations': len(evaluation_manager.evaluations),
            'results': len(evaluation_manager.results),
            'models': len(model_registry.list_models()),
            'active_models': len(model_registry.get_active_models()),
            'completed_evaluations': 0,
            'running_evaluations': 0,
            'pass_rate': 0
        }
        
        # Count completed/running
        for eval_obj in evaluation_manager.evaluations.values():
            if eval_obj.status.value == 'completed':
                stats['completed_evaluations'] += 1
            elif eval_obj.status.value == 'running':
                stats['running_evaluations'] += 1
        
        # Calculate pass rate
        if stats['results'] > 0:
            passed = 0
            for result in evaluation_manager.results.values():
                if result.passed:
                    passed += 1
            stats['pass_rate'] = round((passed / stats['results']) * 100, 1)
        
        # Disk space
        try:
            import shutil
            disk_usage = shutil.disk_usage('.')
            stats['disk_space'] = round(disk_usage.free / (1024**3), 1)
        except:
            stats['disk_space'] = 0
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("AI Model Evaluation API")
    print("=" * 60)
    print("Starting server on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)