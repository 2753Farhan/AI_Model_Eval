# src/managers/evaluation_manager.py

from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

from ..entities import Evaluation, EvaluationResult, Problem
from ..adapters import ModelRegistry
from ..loaders import DatasetLoader
from ..executors import SandboxExecutor
from ..calculators import MetricCalculator
from ..analyzers import ErrorAnalyzer
from ..utils.debug_timer import DebugTimer

logger = logging.getLogger(__name__)


class EvaluationManager:
    def __init__(
        self,
        model_registry: ModelRegistry,
        dataset_loader: DatasetLoader,
        sandbox_executor: SandboxExecutor,
        metric_calculator: MetricCalculator,
        error_analyzer: ErrorAnalyzer,
        max_workers: int = 4
    ):
        self.model_registry = model_registry
        self.dataset_loader = dataset_loader
        self.sandbox = sandbox_executor
        self.metric_calculator = metric_calculator
        self.error_analyzer = error_analyzer
        self.max_workers = max_workers
        
        self.evaluations: Dict[str, Evaluation] = {}
        self.results: Dict[str, EvaluationResult] = {}
        self.progress_callbacks: List[Callable] = []
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
        logger.info(f"EvaluationManager initialized with {max_workers} workers")

    def create_evaluation(
        self,
        user_id: str,
        model_ids: List[str],
        dataset_id: str,
        config: Dict[str, Any]
    ) -> Evaluation:
        """Create a new evaluation"""
        evaluation = Evaluation(user_id=user_id, config=config)
        
        for model_id in model_ids:
            evaluation.add_model(model_id)
        
        evaluation.set_dataset(dataset_id)
        
        self.evaluations[evaluation.evaluation_id] = evaluation
        logger.info(f"Created evaluation {evaluation.evaluation_id}")
        
        return evaluation

    async def run_evaluation(
        self,
        evaluation_id: str,
        progress_callback: Optional[Callable] = None
    ) -> Evaluation:
        """Run an evaluation asynchronously"""
        evaluation = self.evaluations.get(evaluation_id)
        if not evaluation:
            raise ValueError(f"Evaluation {evaluation_id} not found")
        
        if progress_callback:
            self.progress_callbacks.append(progress_callback)
        
        try:
            # Start evaluation
            if not evaluation.start():
                raise RuntimeError("Failed to start evaluation")
            
            self._notify_progress(evaluation, "starting", "Starting evaluation")
            
            # Load dataset
            with DebugTimer("Loading dataset"):
                problems = await self._load_dataset()
                evaluation.update_progress(10, "dataset_loaded")
                self._notify_progress(evaluation, "dataset_loaded", 
                                    f"Loaded {len(problems)} problems")
            
            # Run evaluations for each model
            all_results = []
            total_models = len(evaluation.model_ids)
            
            for model_idx, model_id in enumerate(evaluation.model_ids):
                model_progress_start = 10 + (model_idx / total_models * 60)
                model_progress_end = 10 + ((model_idx + 1) / total_models * 60)
                
                with DebugTimer(f"Evaluating model {model_id}"):
                    model_results = await self._evaluate_model(
                        model_id, problems, evaluation,
                        model_progress_start, model_progress_end
                    )
                    all_results.extend(model_results)
            
            evaluation.update_progress(70, "evaluation_complete")
            self._notify_progress(evaluation, "evaluation_complete",
                                f"Completed {len(all_results)} evaluations")
            
            # Calculate metrics
            with DebugTimer("Calculating metrics"):
                metrics = await self._calculate_metrics(all_results)
                evaluation.update_progress(85, "metrics_calculated")
                self._notify_progress(evaluation, "metrics_calculated", 
                                    f"Calculated metrics")
            
            # Analyze errors
            with DebugTimer("Analyzing errors"):
                error_analysis = await self._analyze_errors(all_results)
                evaluation.update_progress(95, "errors_analyzed")
                self._notify_progress(evaluation, "errors_analyzed",
                                    f"Found {error_analysis.get('total_errors', 0)} errors")
            
            # Store results
            for result in all_results:
                self.results[result.result_id] = result
                evaluation.add_result(result.result_id)
            
            # Complete evaluation
            evaluation.complete()
            evaluation.metadata['metrics'] = metrics
            evaluation.metadata['error_analysis'] = error_analysis
            
            self._notify_progress(evaluation, "completed", 
                                "Evaluation completed successfully")
            
            return evaluation
            
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            evaluation.fail(str(e))
            self._notify_progress(evaluation, "failed", f"Evaluation failed: {e}")
            raise

    async def _load_dataset(self) -> List[Problem]:
        """Load dataset asynchronously"""
        return await asyncio.get_event_loop().run_in_executor(
            self.executor,
            self.dataset_loader.load_dataset
        )

    async def _evaluate_model(
        self,
        model_id: str,
        problems: List[Problem],
        evaluation: Evaluation,
        progress_start: float = 10,
        progress_end: float = 70
    ) -> List[EvaluationResult]:
        """Evaluate a single model on all problems"""
        model = self.model_registry.get_model(model_id)
        if not model:
            raise ValueError(f"Model {model_id} not found")
        
        all_results = []
        total = len(problems)
        num_samples = evaluation.config.get('num_samples', 3)  # Default to 3 samples
        
        # Process in batches for better performance
        batch_size = min(3, max(1, self.max_workers))
        
        for i in range(0, total, batch_size):
            batch = problems[i:i+batch_size]
            
            tasks = []
            for problem in batch:
                for sample_idx in range(num_samples):
                    tasks.append(self._evaluate_one_problem(
                        model, problem, evaluation, sample_idx
                    ))
            
            # Run batch concurrently
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"Error in batch: {result}")
                else:
                    all_results.append(result)
            
            # Update progress
            progress = progress_start + (min(i + batch_size, total) / total * 
                                       (progress_end - progress_start))
            evaluation.update_progress(progress, f"evaluating_{model_id}")
        
        return all_results

    async def _evaluate_one_problem(
        self,
        model,
        problem: Problem,
        evaluation: Evaluation,
        sample_idx: int
    ) -> EvaluationResult:
        """Evaluate a single problem sample"""
        result = EvaluationResult(
            evaluation_id=evaluation.evaluation_id,
            problem_id=problem.problem_id,
            model_id=model.model_name,
            sample_id=sample_idx
        )
        
        try:
            # Get prompt
            prompt = problem.get_prompt()
            
            # Generate code
            with DebugTimer(f"Code generation for {problem.problem_id}"):
                generation_config = evaluation.config.get('generation_config', {})
                generated_code = await model.generate_code(prompt, generation_config)
                
            result.set_generated_code(generated_code)
            
            # Skip execution if generation failed (empty or error)
            if not generated_code or generated_code.startswith('# Error'):
                result.add_error('generation_failed', generated_code if generated_code else 'Empty response')
                return result
            
            # Execute code
            with DebugTimer(f"Code execution for {problem.problem_id}"):
                execution_result = await self.sandbox.execute_safely(
                    generated_code,
                    problem.test_cases,
                    problem.problem_id,
                    language="python",
                    entry_point=problem.entry_point,
                    prompt=problem.prompt
                )
            
            # Set execution results
            result.set_execution_result(
                passed=execution_result.get('passed', False),
                output=execution_result.get('output', ''),
                execution_time_ms=execution_result.get('execution_time_ms', 0)
            )
            
            # Add test results
            for test in execution_result.get('test_results', []):
                result.add_test_result(
                    test_id=test.get('test_id', 0),
                    passed=test.get('passed', False),
                    message=test.get('message', ''),
                    test_case=test.get('test_case')
                )
            
            # Add errors
            for error in execution_result.get('errors', []):
                result.add_error(
                    error_type=error.get('error_type', 'unknown'),
                    error_message=error.get('error_message', '')
                )
            
        except Exception as e:
            logger.error(f"Error in evaluation for problem {problem.problem_id}: {e}")
            result.add_error('evaluation_error', str(e))
        
        return result

    async def _calculate_metrics(self, results: List[EvaluationResult]) -> Dict[str, Any]:
        """Calculate aggregate metrics"""
        try:
            # Check if the calculator has the method we need
            if hasattr(self.metric_calculator, 'calculate_aggregate_metrics'):
                return await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self.metric_calculator.calculate_aggregate_metrics,
                    results
                )
            elif hasattr(self.metric_calculator, 'calculate'):
                # Try calculate method (some calculators use this)
                metrics = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self.metric_calculator.calculate,
                    results
                )
                # Enhance with additional stats
                metrics.update(self._get_basic_stats(results))
                return metrics
            else:
                # Manual calculation
                return self._calculate_metrics_fallback(results)
        except Exception as e:
            logger.error(f"Metrics calculation failed: {e}")
            return self._calculate_metrics_fallback(results)

    def _get_basic_stats(self, results: List[EvaluationResult]) -> Dict[str, Any]:
        """Get basic statistics from results"""
        if not results:
            return {}
        
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        
        return {
            'total_results': total,
            'passed_results': passed,
            'pass_rate': passed / total if total > 0 else 0,
            'failed_results': total - passed
        }

    def _calculate_metrics_fallback(self, results: List[EvaluationResult]) -> Dict[str, Any]:
        """Fallback metrics calculation when calculator methods fail"""
        if not results:
            return {}
        
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        
        # Group by model
        model_stats = defaultdict(lambda: {'total': 0, 'passed': 0})
        for r in results:
            model_stats[r.model_id]['total'] += 1
            if r.passed:
                model_stats[r.model_id]['passed'] += 1
        
        # Calculate pass rates per model
        by_model = {}
        for model_id, stats in model_stats.items():
            by_model[model_id] = {
                'pass_rate': stats['passed'] / stats['total'] if stats['total'] > 0 else 0,
                'total': stats['total'],
                'passed': stats['passed']
            }
        
        # Execution time stats
        exec_times = [r.execution_time_ms for r in results if r.execution_time_ms]
        
        return {
            'total_results': total,
            'passed_results': passed,
            'pass_rate': passed / total if total > 0 else 0,
            'failed_results': total - passed,
            'total_errors': sum(len(r.errors) for r in results),
            'avg_execution_time_ms': sum(exec_times) / len(exec_times) if exec_times else 0,
            'by_model': by_model
        }

    async def _analyze_errors(self, results: List[EvaluationResult]) -> Dict[str, Any]:
        """Analyze errors across results"""
        try:
            all_errors = []
            for result in results:
                all_errors.extend(result.errors)
            
            if hasattr(self.error_analyzer, 'analyze_errors'):
                return await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self.error_analyzer.analyze_errors,
                    all_errors
                )
            else:
                # Simple error analysis
                error_types = {}
                for error in all_errors:
                    error_type = error.get('error_type', 'unknown')
                    error_types[error_type] = error_types.get(error_type, 0) + 1
                
                return {
                    'total_errors': len(all_errors),
                    'error_types': error_types,
                    'has_errors': len(all_errors) > 0
                }
        except Exception as e:
            logger.error(f"Error analysis failed: {e}")
            return {
                'total_errors': sum(len(r.errors) for r in results),
                'error': str(e)
            }

    def _notify_progress(self, evaluation: Evaluation, stage: str, message: str, data: Optional[Dict] = None):
        """Notify progress callbacks"""
        for callback in self.progress_callbacks:
            try:
                callback(
                    evaluation.evaluation_id,
                    stage,
                    message,
                    {
                        'progress': evaluation.progress,
                        'current_stage': evaluation.current_stage,
                        'data': data or {}
                    }
                )
            except Exception as e:
                logger.error(f"Progress callback failed: {e}")

    def get_evaluation(self, evaluation_id: str) -> Optional[Evaluation]:
        """Get evaluation by ID"""
        return self.evaluations.get(evaluation_id)

    def get_results(self, evaluation_id: str) -> List[EvaluationResult]:
        """Get all results for an evaluation"""
        evaluation = self.evaluations.get(evaluation_id)
        if not evaluation:
            return []
        
        return [
            self.results[result_id]
            for result_id in evaluation.results_ids
            if result_id in self.results
        ]

    def cancel_evaluation(self, evaluation_id: str) -> bool:
        """Cancel an evaluation"""
        evaluation = self.evaluations.get(evaluation_id)
        if not evaluation:
            return False
        return evaluation.cancel()

    def get_evaluation_summary(self, evaluation_id: str) -> Dict[str, Any]:
        """Get summary of evaluation results"""
        evaluation = self.get_evaluation(evaluation_id)
        results = self.get_results(evaluation_id)
        
        if not evaluation:
            return {'error': 'Evaluation not found'}
        
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        
        return {
            'evaluation_id': evaluation_id,
            'status': evaluation.status.value if hasattr(evaluation.status, 'value') else str(evaluation.status),
            'total_samples': total,
            'passed_samples': passed,
            'pass_rate': passed / total if total > 0 else 0,
            'models_tested': len(set(r.model_id for r in results)),
            'problems_tested': len(set(r.problem_id for r in results)),
            'duration_seconds': evaluation.get_duration(),
            'created_at': evaluation.created_at.isoformat() if evaluation.created_at else None
        }