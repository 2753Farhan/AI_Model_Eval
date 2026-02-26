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
import logging
import traceback
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add src to path
sys.path.append(str(Path(__file__).parent))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
from src.entities import  EvaluationResult
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
from datetime import datetime, timedelta
import secrets
from pathlib import Path
from flask import send_file
from src.entities import Benchmark

# Initialize config first
from src.config.config_manager import ConfigManager
config = ConfigManager("config/settings.yaml")

# ==================== FINE-TUNING IMPORTS (SINGLE INSTANCE) ====================
finetuning_available = False
failure_analyzer = None
dataset_preparer = None
ollama_trainer = None

try:
    from src.finetuning import FailureAnalyzer, DatasetPreparer, OllamaTrainer
    finetuning_available = True
    print("✅ Fine-tuning modules loaded successfully")
    
    # Initialize with config
    failure_analyzer = FailureAnalyzer(config)  # Pass config here!
    dataset_preparer = DatasetPreparer()
    ollama_trainer = OllamaTrainer()
    
except ImportError as e:
    print(f"⚠️ Fine-tuning modules not available: {e}")
    print("Some fine-tuning features will be disabled")
    
    # Create dummy classes if modules not available
    class DummyFailureAnalyzer:
        def __init__(self, config=None):
            self.config = config
        
        def analyze_evaluation(self, results):
            return {'error': 'Fine-tuning not available'}
    
    class DummyDatasetPreparer:
        def find_similar_problems(self, *args, **kwargs):
            return []
        def create_training_data(self, *args, **kwargs):
            return None
    
    class DummyOllamaTrainer:
        def fine_tune(self, *args, **kwargs):
            return {'success': False, 'error': 'Fine-tuning not available'}
        def list_finetuned_models(self):
            return []
    
    # Initialize dummy classes
    failure_analyzer = DummyFailureAnalyzer(config)
    dataset_preparer = DummyDatasetPreparer()
    ollama_trainer = DummyOllamaTrainer()

# Initialize components
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


# ==================== DATASET DETAIL APIs ====================

@app.route('/api/datasets/<dataset_id>', methods=['GET', 'OPTIONS'])
def get_dataset_info(dataset_id):
    """Get detailed information about a specific dataset"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        if dataset_id != 'humaneval':
            return jsonify({'error': 'Dataset not found'}), 404
        
        problems = dataset_loader.load_dataset()
        
        # Calculate dataset statistics
        total_problems = len(problems)
        languages = {}
        difficulties = {'easy': 0, 'medium': 0, 'hard': 0}
        test_cases_total = 0
        
        for problem in problems:
            # Count languages
            lang = problem.metadata.get('language', 'python')
            languages[lang] = languages.get(lang, 0) + 1
            
            # Estimate difficulty based on complexity
            complexity = problem.stats.get('cyclomatic_complexity', 0) if problem.stats else 0
            if complexity <= 3:
                difficulties['easy'] += 1
            elif complexity <= 7:
                difficulties['medium'] += 1
            else:
                difficulties['hard'] += 1
            
            test_cases_total += len(problem.test_cases)
        
        dataset_info = {
            'id': dataset_id,
            'name': 'HumanEval',
            'description': 'OpenAI HumanEval dataset for code generation evaluation',
            'source': 'OpenAI',
            'paper': 'Evaluating Large Language Models Trained on Code',
            'year': 2021,
            'total_problems': total_problems,
            'languages': languages,
            'difficulties': difficulties,
            'avg_test_cases': test_cases_total / total_problems if total_problems > 0 else 0,
            'total_test_cases': test_cases_total,
            'license': 'MIT',
            'citation': '@article{chen2021codex,\n  title={Evaluating Large Language Models Trained on Code},\n  author={Mark Chen and others},\n  year={2021},\n  eprint={2107.03374},\n  archivePrefix={arXiv}\n}'
        }
        
        return jsonify(dataset_info)
        
    except Exception as e:
        logger.error(f"Error getting dataset info: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/datasets/<dataset_id>/samples', methods=['GET', 'OPTIONS'])
def get_dataset_samples(dataset_id):
    """Get paginated samples from a dataset"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        if dataset_id != 'humaneval':
            return jsonify({'error': 'Dataset not found'}), 404
        
        # Pagination parameters
        limit = request.args.get('limit', default=50, type=int)
        offset = request.args.get('offset', default=0, type=int)
        
        problems = dataset_loader.load_dataset()
        total = len(problems)
        
        # Apply pagination
        paginated_problems = problems[offset:offset + limit]
        
        samples = []
        for problem in paginated_problems:
            # Calculate basic metrics for each sample
            metrics = {}
            if problem.canonical_solution:
                quality_metrics = quality_calculator.calculate_per_file(problem.canonical_solution)
                metrics.update(quality_metrics)
                metrics['quality_grade'] = quality_calculator.grade_quality(quality_metrics)
            
            samples.append({
                'problem_id': problem.problem_id,
                'task_id': problem.task_id,
                'entry_point': problem.entry_point,
                'prompt_preview': problem.prompt[:200] + '...' if len(problem.prompt) > 200 else problem.prompt,
                'difficulty': estimate_difficulty(problem),
                'test_count': len(problem.test_cases),
                'language': problem.metadata.get('language', 'python'),
                'metrics': metrics,
                'has_solution': problem.canonical_solution is not None
            })
        
        return jsonify({
            'total': total,
            'offset': offset,
            'limit': limit,
            'samples': samples
        })
        
    except Exception as e:
        logger.error(f"Error getting dataset samples: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/datasets/<dataset_id>/samples/<sample_id>', methods=['GET', 'OPTIONS'], endpoint='get_dataset_sample_detail')
def get_dataset_sample_detail(dataset_id, sample_id):
    """Get detailed information about a specific sample"""
    if request.method == 'OPTIONS':
        return '', 204
    
    # Import logger if not available
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        if dataset_id != 'humaneval':
            return jsonify({'error': 'Dataset not found'}), 404
        
        problems = dataset_loader.load_dataset()
        logger.info(f"Looking for sample {sample_id} in {len(problems)} problems")
        
        # Find the problem by ID with multiple strategies
        problem = None
        for p in problems:
            # Get all possible identifiers
            p_id = getattr(p, 'problem_id', '')
            t_id = getattr(p, 'task_id', '')
            
            # Check matches
            if p_id == sample_id or t_id == sample_id:
                problem = p
                break
            
            # Check if sample_id ends with task_id (for prob_ format)
            if t_id and (t_id.endswith(sample_id) or sample_id.endswith(t_id)):
                problem = p
                break
            
            # Check if sample_id contains task_id
            if t_id and t_id.replace('/', '_') in sample_id:
                problem = p
                break
        
        if not problem:
            # Log available IDs for debugging
            available = []
            for p in problems[:20]:  # First 20
                available.append({
                    'problem_id': getattr(p, 'problem_id', 'N/A'),
                    'task_id': getattr(p, 'task_id', 'N/A')
                })
            logger.error(f"Sample {sample_id} not found. Available samples: {available}")
            return jsonify({'error': f'Sample not found'}), 404
        
        # Safely get attributes with defaults
        def safe_get(obj, attr, default=None):
            return getattr(obj, attr, default) if obj else default
        
        # Get problem data safely
        problem_id = safe_get(problem, 'problem_id', sample_id)
        task_id = safe_get(problem, 'task_id', 'unknown')
        entry_point = safe_get(problem, 'entry_point', 'unknown')
        prompt = safe_get(problem, 'prompt', '')
        canonical_solution = safe_get(problem, 'canonical_solution', '')
        
        # Handle test data - Problem objects might store tests differently
        test_data = ''
        if hasattr(problem, 'test'):
            test_data = problem.test
        elif hasattr(problem, 'test_code'):
            test_data = problem.test_code
        elif hasattr(problem, 'tests'):
            test_data = str(problem.tests)
        
        # Get test cases safely
        test_cases = safe_get(problem, 'test_cases', [])
        categories = safe_get(problem, 'categories', [])
        metadata = safe_get(problem, 'metadata', {})
        stats = safe_get(problem, 'stats', {})
        
        # Calculate comprehensive metrics
        metrics = {}
        if canonical_solution:
            try:
                quality_metrics = quality_calculator.calculate_per_file(canonical_solution)
                metrics.update(quality_metrics)
                metrics['quality_grade'] = quality_calculator.grade_quality(quality_metrics)
            except Exception as e:
                logger.error(f"Error calculating metrics: {e}")
                metrics = {'error': str(e)}
        
        # Format test cases safely
        formatted_test_cases = []
        for i, tc in enumerate(test_cases):
            if isinstance(tc, dict):
                formatted_test_cases.append({
                    'assertion': tc.get('assertion', ''),
                    'type': tc.get('type', 'assert'),
                    'description': f"Test case {i + 1}"
                })
            elif isinstance(tc, str):
                formatted_test_cases.append({
                    'assertion': tc,
                    'type': 'assert',
                    'description': f"Test case {i + 1}"
                })
            else:
                formatted_test_cases.append({
                    'assertion': str(tc),
                    'type': 'assert',
                    'description': f"Test case {i + 1}"
                })
        
        # Estimate difficulty
        difficulty = 'unknown'
        if stats:
            complexity = stats.get('cyclomatic_complexity', 0)
            if complexity <= 3:
                difficulty = 'easy'
            elif complexity <= 7:
                difficulty = 'medium'
            else:
                difficulty = 'hard'
        
        sample_detail = {
            'problem_id': problem_id,
            'task_id': task_id,
            'entry_point': entry_point,
            'prompt': prompt,
            'canonical_solution': canonical_solution,
            'test_code': test_data,
            'test_cases': formatted_test_cases,
            'difficulty': difficulty,
            'language': metadata.get('language', 'python'),
            'tags': categories,
            'metrics': metrics,
            'stats': stats
        }
        
        return jsonify(sample_detail)
        
    except Exception as e:
        # Create logger if not available
        if 'logger' not in locals():
            import logging
            logger = logging.getLogger(__name__)
        
        logger.error(f"Error getting sample: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/datasets/<dataset_id>/stats', methods=['GET', 'OPTIONS'])
def get_dataset_statistics(dataset_id):
    """Get comprehensive statistics about a dataset"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        if dataset_id != 'humaneval':
            return jsonify({'error': 'Dataset not found'}), 404
        
        problems = dataset_loader.load_dataset()
        
        # Initialize statistics
        stats = {
            'total_problems': len(problems),
            'languages': {},
            'difficulties': {'easy': 0, 'medium': 0, 'hard': 0},
            'test_cases': {
                'total': 0,
                'avg_per_problem': 0,
                'distribution': []
            },
            'complexity': {
                'avg_cyclomatic': 0,
                'avg_lines': 0,
                'distribution': {}
            },
            'categories': {},
            'tags': {},
            'solution_stats': {
                'has_solution': 0,
                'avg_solution_length': 0,
                'total_solutions': 0
            }
        }
        
        total_complexity = 0
        total_lines = 0
        solution_lengths = []
        
        for problem in problems:
            # Language stats
            lang = problem.metadata.get('language', 'python')
            stats['languages'][lang] = stats['languages'].get(lang, 0) + 1
            
            # Difficulty estimation
            complexity = problem.stats.get('cyclomatic_complexity', 0) if problem.stats else 0
            if complexity <= 3:
                stats['difficulties']['easy'] += 1
            elif complexity <= 7:
                stats['difficulties']['medium'] += 1
            else:
                stats['difficulties']['hard'] += 1
            
            # Test cases
            tc_count = len(problem.test_cases)
            stats['test_cases']['total'] += tc_count
            stats['test_cases']['distribution'].append(tc_count)
            
            # Complexity
            if problem.stats:
                total_complexity += problem.stats.get('cyclomatic_complexity', 0)
                total_lines += problem.stats.get('loc', 0)
            
            # Categories/tags
            for cat in problem.categories:
                stats['categories'][cat] = stats['categories'].get(cat, 0) + 1
            
            # Solutions
            if problem.canonical_solution:
                stats['solution_stats']['has_solution'] += 1
                solution_lengths.append(len(problem.canonical_solution))
        
        # Calculate averages
        if problems:
            stats['test_cases']['avg_per_problem'] = stats['test_cases']['total'] / len(problems)
            stats['complexity']['avg_cyclomatic'] = total_complexity / len(problems)
            stats['complexity']['avg_lines'] = total_lines / len(problems)
            
            # Complexity distribution
            complexity_values = [p.stats.get('cyclomatic_complexity', 0) if p.stats else 0 for p in problems]
            stats['complexity']['distribution'] = {
                'min': min(complexity_values),
                'max': max(complexity_values),
                'median': sorted(complexity_values)[len(complexity_values)//2]
            }
            
            # Solution stats
            if solution_lengths:
                stats['solution_stats']['avg_solution_length'] = sum(solution_lengths) / len(solution_lengths)
                stats['solution_stats']['total_solutions'] = len(solution_lengths)
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error getting dataset statistics: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/datasets/<dataset_id>/search', methods=['GET', 'OPTIONS'])
def search_dataset(dataset_id):
    """Search for samples in a dataset"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        if dataset_id != 'humaneval':
            return jsonify({'error': 'Dataset not found'}), 404
        
        query = request.args.get('q', '').lower()
        if not query or len(query) < 2:
            return jsonify({'error': 'Search query must be at least 2 characters'}), 400
        
        problems = dataset_loader.load_dataset()
        
        results = []
        for problem in problems:
            score = 0
            
            # Search in task_id
            if query in problem.task_id.lower():
                score += 10
            
            # Search in prompt
            if query in problem.prompt.lower():
                score += 5
            
            # Search in entry_point
            if problem.entry_point and query in problem.entry_point.lower():
                score += 8
            
            # Search in categories
            for cat in problem.categories:
                if query in cat.lower():
                    score += 3
            
            if score > 0:
                results.append({
                    'problem_id': problem.problem_id,
                    'task_id': problem.task_id,
                    'entry_point': problem.entry_point,
                    'prompt_preview': problem.prompt[:150] + '...' if len(problem.prompt) > 150 else problem.prompt,
                    'relevance_score': score,
                    'test_count': len(problem.test_cases),
                    'difficulty': estimate_difficulty(problem)
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return jsonify({
            'query': query,
            'total_results': len(results),
            'results': results[:50]  # Limit to 50 results
        })
        
    except Exception as e:
        logger.error(f"Error searching dataset: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/datasets/<dataset_id>/samples/<sample_id>/execute', methods=['POST', 'OPTIONS'], endpoint='execute_sample')
def execute_sample(dataset_id, sample_id):
    """Execute a sample's canonical solution in the sandbox"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        if dataset_id != 'humaneval':
            return jsonify({'error': 'Dataset not found'}), 404
        
        problems = dataset_loader.load_dataset()
        
        # Find the problem
        problem = None
        for p in problems:
            p_id = getattr(p, 'problem_id', '')
            t_id = getattr(p, 'task_id', '')
            if p_id == sample_id or t_id == sample_id:
                problem = p
                break
        
        if not problem:
            return jsonify({'error': 'Sample not found'}), 404
        
        if not problem.canonical_solution:
            return jsonify({'error': 'No canonical solution available'}), 400
        
        # Format the code
        from src.utils.code_formatter import CodeFormatter
        
        formatted_code = CodeFormatter.prepare_for_execution(
            code=problem.canonical_solution,
            entry_point=problem.entry_point,
            prompt=problem.prompt,
            is_canonical=True
        )
        
        # Format test cases
        formatted_test_cases = CodeFormatter.prepare_test_cases_for_execution(
            problem.test_cases, problem.entry_point
        )
        
        # Execute the formatted solution
        async def run_solution():
            return await sandbox.execute_safely(
                code=formatted_code,
                test_cases=formatted_test_cases,
                problem_id=problem.problem_id,
                language='python'
            )
        
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_solution())
        loop.close()
        
        # Add sample metadata
        result['task_id'] = problem.task_id
        result['entry_point'] = problem.entry_point
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error executing sample: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/datasets/<dataset_id>/samples/<sample_id>/metrics', methods=['POST', 'OPTIONS'], endpoint='analyze_sample_metrics')
def analyze_sample_metrics(dataset_id, sample_id):
    """Calculate comprehensive metrics for a sample's solution"""
    if request.method == 'OPTIONS':
        return '', 204
    
    # Create logger if not available
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        if dataset_id != 'humaneval':
            return jsonify({'error': 'Dataset not found'}), 404
        
        problems = dataset_loader.load_dataset()
        
        # Find the problem
        problem = None
        for p in problems:
            p_id = getattr(p, 'problem_id', '')
            t_id = getattr(p, 'task_id', '')
            if p_id == sample_id or t_id == sample_id:
                problem = p
                break
        
        if not problem:
            return jsonify({'error': 'Sample not found'}), 404
        
        # Get problem data
        canonical_solution = getattr(problem, 'canonical_solution', '')
        entry_point = getattr(problem, 'entry_point', 'solution')
        prompt = getattr(problem, 'prompt', '')
        test_cases = getattr(problem, 'test_cases', [])
        problem_id = getattr(problem, 'problem_id', sample_id)
        
        if not canonical_solution:
            return jsonify({'error': 'No canonical solution available'}), 400
        
        # Format the code using CodeFormatter
        from src.utils.code_formatter import CodeFormatter
        
        formatted_code = CodeFormatter.prepare_for_execution(
            code=canonical_solution,
            entry_point=entry_point,
            prompt=prompt,
            is_canonical=True
        )
        
        # Calculate metrics on formatted code
        metrics = {}
        
        # Quality metrics
        try:
            quality_metrics = quality_calculator.calculate_per_file(formatted_code)
            metrics.update(quality_metrics)
            metrics['quality_grade'] = quality_calculator.grade_quality(quality_metrics)
        except Exception as e:
            logger.error(f"Error calculating quality metrics: {e}")
            metrics['quality_error'] = str(e)
        
        # Basic metrics
        lines = formatted_code.split('\n')
        metrics['total_lines'] = len(lines)
        metrics['blank_lines'] = sum(1 for line in lines if line.strip() == '')
        metrics['code_lines'] = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
        metrics['comment_lines'] = sum(1 for line in lines if line.strip().startswith('#'))
        
        # Function and class counts
        metrics['function_count'] = formatted_code.count('def ')
        metrics['class_count'] = formatted_code.count('class ')
        
        # Execute the formatted code to get test results
        test_results = None
        try:
            async def run_tests():
                # Format code the same way as execute endpoint
                exec_code = CodeFormatter.prepare_for_execution(
                    code=canonical_solution,
                    entry_point=entry_point,
                    prompt=prompt,
                    is_canonical=True
                )

                # Format test cases the same way as execute endpoint
                exec_test_cases = CodeFormatter.prepare_test_cases_for_execution(
                    test_cases, entry_point
                )

                return await sandbox.execute_safely(
                    code=exec_code,
                    test_cases=exec_test_cases,
                    problem_id=problem_id,
                    language='python'
                )            
            # Run the async function
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            test_results = loop.run_until_complete(run_tests())
            loop.close()
            
            if test_results and 'test_results' in test_results:
                passed = sum(1 for t in test_results['test_results'] if t.get('passed'))
                total = len(test_results['test_results'])
                metrics['test_pass_rate'] = passed / total if total > 0 else 0
                metrics['tests_passed'] = passed
                metrics['tests_total'] = total
            else:
                metrics['test_pass_rate'] = 0
                metrics['tests_passed'] = 0
                metrics['tests_total'] = len(test_cases)
                
        except Exception as e:
            logger.error(f"Error running tests: {e}")
            metrics['test_pass_rate'] = 0
            metrics['tests_passed'] = 0
            metrics['tests_total'] = len(test_cases)
            test_results = {'error': str(e), 'passed': False}
        
        return jsonify({
            'task_id': getattr(problem, 'task_id', 'unknown'),
            'entry_point': entry_point,
            'metrics': metrics,
            'test_results': test_results,
            'formatted_code': formatted_code  # Optional: return for debugging
        })
        
    except Exception as e:
        logger.error(f"Error analyzing sample metrics: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/datasets/<dataset_id>/samples/<sample_id>/test', methods=['POST', 'OPTIONS'])
def test_sample_with_custom_code(dataset_id, sample_id):
    """Test a sample with custom code provided by the user"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        if dataset_id != 'humaneval':
            return jsonify({'error': 'Dataset not found'}), 404
        
        data = request.json
        custom_code = data.get('code', '')
        
        if not custom_code:
            return jsonify({'error': 'No code provided'}), 400
        
        problems = dataset_loader.load_dataset()
        
        # Find the problem
        problem = None
        for p in problems:
            if p.problem_id == sample_id or p.task_id == sample_id:
                problem = p
                break
        
        if not problem:
            return jsonify({'error': 'Sample not found'}), 404
        
        # Execute custom code
        async def run_custom():
            return await sandbox.execute_safely(
                code=custom_code,
                test_cases=problem.test_cases,
                problem_id=problem.problem_id,
                language='python'
            )
        
        result = run_async(run_custom())
        
        # Add metadata
        result['task_id'] = problem.task_id
        result['entry_point'] = problem.entry_point
        result['test_count'] = len(problem.test_cases)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error testing custom code: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/datasets/<dataset_id>/random', methods=['GET', 'OPTIONS'])
def get_random_sample(dataset_id):
    """Get a random sample from the dataset"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        if dataset_id != 'humaneval':
            return jsonify({'error': 'Dataset not found'}), 404
        
        problems = dataset_loader.load_dataset()
        import random
        problem = random.choice(problems)
        
        return jsonify({
            'problem_id': problem.problem_id,
            'task_id': problem.task_id,
            'entry_point': problem.entry_point,
            'prompt_preview': problem.prompt[:200] + '...' if len(problem.prompt) > 200 else problem.prompt,
            'difficulty': estimate_difficulty(problem),
            'test_count': len(problem.test_cases)
        })
        
    except Exception as e:
        logger.error(f"Error getting random sample: {e}")
        return jsonify({'error': str(e)}), 500


# Helper function to estimate difficulty
def estimate_difficulty(problem):
    """Estimate problem difficulty based on complexity"""
    if problem.stats:
        complexity = problem.stats.get('cyclomatic_complexity', 0)
        if complexity <= 3:
            return 'easy'
        elif complexity <= 7:
            return 'medium'
        else:
            return 'hard'
    return 'unknown'


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
    

# ==================== REPORT GENERATION APIS ====================

@app.route('/api/reports/generate/<evaluation_id>', methods=['POST', 'OPTIONS'])
def generate_report(evaluation_id):
    """Generate a report for an evaluation"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json or {}
        report_type = data.get('report_type', 'summary')  # summary, detailed, comparative
        format = data.get('format', 'html')  # html, pdf, json, csv, md
        
        # Get evaluation and results
        evaluation = evaluation_manager.get_evaluation(evaluation_id)
        if not evaluation:
            return jsonify({'error': 'Evaluation not found'}), 404
        
        results = evaluation_manager.get_results(evaluation_id)
        if not results:
            return jsonify({'error': 'No results found for evaluation'}), 404
        
        # Initialize report generator
        report_generator = ReportGenerator(config={
            'output_dir': 'reports',
            'company_name': 'AI Model Eval',
            'include_charts': True
        })
        
        # Generate report based on type
        if report_type == 'summary':
            report = report_generator.generate_summary_report(evaluation, results, format)
        elif report_type == 'detailed':
            report = report_generator.generate_detailed_report(evaluation, results, format)
        else:
            return jsonify({'error': f'Unsupported report type: {report_type}'}), 400
        
        # Return report info
        return jsonify({
            'success': True,
            'report_id': report.report_id,
            'evaluation_id': report.evaluation_id,
            'report_type': report.report_type,
            'format': report.format,
            'file_path': report.file_path,
            'generated_at': report.generated_at.isoformat(),
            'download_url': f"/api/reports/download/{report.report_id}"
        })
        
    except Exception as e:
        print(f"Error generating report: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/compare', methods=['POST', 'OPTIONS'])
def generate_comparative_report():
    """Generate a comparative report across multiple evaluations"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        evaluation_ids = data.get('evaluation_ids', [])
        format = data.get('format', 'html')
        benchmark_name = data.get('benchmark_name', 'Comparative Analysis')
        
        if len(evaluation_ids) < 2:
            return jsonify({'error': 'At least 2 evaluation IDs required'}), 400
        
        # Get evaluations and results
        evaluations = []
        results_dict = {}
        
        for eval_id in evaluation_ids:
            evaluation = evaluation_manager.get_evaluation(eval_id)
            if not evaluation:
                return jsonify({'error': f'Evaluation not found: {eval_id}'}), 404
            
            results = evaluation_manager.get_results(eval_id)
            if not results:
                return jsonify({'error': f'No results found for evaluation: {eval_id}'}), 404
            
            evaluations.append(evaluation)
            results_dict[eval_id] = results
        
        # Create a benchmark object
        from src.entities import Benchmark
        benchmark = Benchmark(
            benchmark_id=f"cmp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            name=benchmark_name,
            description=f"Comparative analysis of {len(evaluation_ids)} evaluations"
        )
        
        # Add models and results to benchmark
        for eval_id, results in results_dict.items():
            for result in results:
                benchmark.add_result(result.model_id, result)
        
        # Calculate rankings
        benchmark.calculate_rankings()
        
        # Initialize report generator
        report_generator = ReportGenerator(config={
            'output_dir': 'reports/comparative',
            'include_charts': True
        })
        
        # Generate comparative report
        report = report_generator.generate_comparative_report(
            evaluations=evaluations,
            results_dict=results_dict,
            benchmark=benchmark,
            format=format
        )
        
        return jsonify({
            'success': True,
            'report_id': report.report_id,
            'benchmark_id': benchmark.benchmark_id,
            'evaluations': evaluation_ids,
            'format': format,
            'file_path': report.file_path,
            'generated_at': report.generated_at.isoformat(),
            'download_url': f"/api/reports/download/{report.report_id}"
        })
        
    except Exception as e:
        print(f"Error generating comparative report: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/list', methods=['GET', 'OPTIONS'])
def list_reports():
    """List all generated reports"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        reports_dir = Path('reports')
        if not reports_dir.exists():
            return jsonify([])
        
        reports = []
        for file_path in reports_dir.glob('**/*'):
            if file_path.is_file():
                # Parse report info from filename
                filename = file_path.name
                parts = filename.split('_')
                
                report_info = {
                    'filename': filename,
                    'file_path': str(file_path),
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'download_url': f"/api/reports/download/{file_path.name}",
                    'format': file_path.suffix[1:] if file_path.suffix else 'unknown'
                }
                
                # Try to extract evaluation ID from filename
                if len(parts) >= 3 and parts[0] == 'report':
                    report_info['evaluation_id'] = parts[1]
                    report_info['report_type'] = parts[2]
                
                reports.append(report_info)
        
        # Sort by modified date, newest first
        reports.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify(reports)
        
    except Exception as e:
        print(f"Error listing reports: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/download/<filename>', methods=['GET', 'OPTIONS'])
def download_report(filename):
    """Download a generated report file"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Search for the file in reports directory
        reports_dir = Path('reports')
        for file_path in reports_dir.rglob(filename):
            if file_path.is_file():
                return send_file(
                    str(file_path),
                    as_attachment=True,
                    download_name=filename,
                    mimetype=get_mimetype(file_path.suffix)
                )
        
        return jsonify({'error': 'Report not found'}), 404
        
    except Exception as e:
        print(f"Error downloading report: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/preview/<evaluation_id>', methods=['GET', 'OPTIONS'])
def preview_report(evaluation_id):
    """Preview a report without saving to file"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        report_type = request.args.get('type', 'summary')
        
        # Get evaluation and results
        evaluation = evaluation_manager.get_evaluation(evaluation_id)
        if not evaluation:
            return jsonify({'error': 'Evaluation not found'}), 404
        
        results = evaluation_manager.get_results(evaluation_id)
        if not results:
            return jsonify({'error': 'No results found for evaluation'}), 404
        
        # Initialize report generator
        report_generator = ReportGenerator(config={'include_charts': True})
        
        # Generate preview data without saving
        if report_type == 'summary':
            summary_data = report_generator._prepare_summary_data(evaluation, results)
            charts = report_generator._generate_summary_charts(results)
            tables = report_generator._generate_summary_tables(results)
        elif report_type == 'detailed':
            summary_data = report_generator._prepare_detailed_data(evaluation, results)
            charts = report_generator._generate_detailed_charts(results)
            tables = report_generator._generate_detailed_tables(results)
        else:
            return jsonify({'error': f'Unsupported report type: {report_type}'}), 400
        
        return jsonify({
            'success': True,
            'evaluation_id': evaluation_id,
            'report_type': report_type,
            'summary': summary_data,
            'charts': charts,
            'tables': tables
        })
        
    except Exception as e:
        print(f"Error previewing report: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/schedule', methods=['POST', 'OPTIONS'])
def schedule_report():
    """Schedule automatic report generation"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        evaluation_id = data.get('evaluation_id')
        schedule_type = data.get('schedule_type', 'daily')  # daily, weekly, monthly
        report_types = data.get('report_types', ['summary'])
        formats = data.get('formats', ['html'])
        email = data.get('email')  # Optional email to send reports to
        
        # Store schedule in database or file
        schedule_id = f"schedule_{secrets.token_hex(8)}"
        
        schedule_data = {
            'schedule_id': schedule_id,
            'evaluation_id': evaluation_id,
            'schedule_type': schedule_type,
            'report_types': report_types,
            'formats': formats,
            'email': email,
            'created_at': datetime.now().isoformat(),
            'next_run': calculate_next_run(schedule_type)
        }
        
        # Save to file (you might want to use a real database)
        schedules_file = Path('reports/schedules.json')
        if schedules_file.exists():
            with open(schedules_file, 'r') as f:
                schedules = json.load(f)
        else:
            schedules = []
        
        schedules.append(schedule_data)
        
        with open(schedules_file, 'w') as f:
            json.dump(schedules, f, indent=2)
        
        return jsonify({
            'success': True,
            'schedule_id': schedule_id,
            'message': f'Report scheduled {schedule_type}',
            'next_run': schedule_data['next_run']
        })
        
    except Exception as e:
        print(f"Error scheduling report: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/export/<evaluation_id>/<format>', methods=['GET', 'OPTIONS'])
def export_report_format(evaluation_id, format):
    """Export report directly in specified format"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        report_type = request.args.get('type', 'summary')
        
        # Get evaluation and results
        evaluation = evaluation_manager.get_evaluation(evaluation_id)
        if not evaluation:
            return jsonify({'error': 'Evaluation not found'}), 404
        
        results = evaluation_manager.get_results(evaluation_id)
        if not results:
            return jsonify({'error': 'No results found for evaluation'}), 404
        
        # Initialize report generator
        report_generator = ReportGenerator(config={'output_dir': 'temp'})
        
        # Generate report
        if report_type == 'summary':
            report = report_generator.generate_summary_report(evaluation, results, format)
        elif report_type == 'detailed':
            report = report_generator.generate_detailed_report(evaluation, results, format)
        else:
            return jsonify({'error': f'Unsupported report type: {report_type}'}), 400
        
        # Read the file and send
        if report.file_path and Path(report.file_path).exists():
            return send_file(
                report.file_path,
                as_attachment=True,
                download_name=f"report_{evaluation_id}_{report_type}.{format}",
                mimetype=get_mimetype(f'.{format}')
            )
        else:
            return jsonify({'error': 'Report file not found'}), 404
        
    except Exception as e:
        print(f"Error exporting report: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# Helper function for mimetypes
def get_mimetype(extension):
    """Get mimetype for file extension"""
    mimetypes = {
        '.html': 'text/html',
        '.pdf': 'application/pdf',
        '.json': 'application/json',
        '.csv': 'text/csv',
        '.md': 'text/markdown',
        '.txt': 'text/plain'
    }
    return mimetypes.get(extension.lower(), 'application/octet-stream')


def calculate_next_run(schedule_type):
    """Calculate next run time based on schedule type"""
    now = datetime.now()
    
    if schedule_type == 'daily':
        next_run = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
    elif schedule_type == 'weekly':
        # Next Monday
        days_ahead = 7 - now.weekday()
        next_run = now.replace(hour=0, minute=0, second=0) + timedelta(days=days_ahead)
    elif schedule_type == 'monthly':
        # First day of next month
        if now.month == 12:
            next_run = now.replace(year=now.year+1, month=1, day=1, hour=0, minute=0, second=0)
        else:
            next_run = now.replace(month=now.month+1, day=1, hour=0, minute=0, second=0)
    else:
        next_run = now + timedelta(hours=1)  # Default: hourly
    
    return next_run.isoformat()

if __name__ == '__main__':
    print("=" * 60)
    print("AI Model Evaluation API")
    print("=" * 60)
    print("Starting server on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)