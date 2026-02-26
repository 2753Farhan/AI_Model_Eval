# src/calculators/functional_metrics.py

from typing import List, Dict, Any, Optional
import numpy as np
from collections import defaultdict
import logging

from .metric_calculator import MetricCalculator
from ..entities import EvaluationResult, Metric

logger = logging.getLogger(__name__)


class FunctionalMetricsCalculator(MetricCalculator):
    """Calculator for functional correctness metrics"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.supported_metrics = ['pass_rate', 'pass@1', 'pass@5', 'pass@10', 'error_rate']
        
        # Set normalization rules
        self.set_normalization_rule('pass_rate', 0, 1, higher_is_better=True)
        self.set_normalization_rule('pass@1', 0, 1, higher_is_better=True)
        self.set_normalization_rule('pass@5', 0, 1, higher_is_better=True)
        self.set_normalization_rule('pass@10', 0, 1, higher_is_better=True)
        self.set_normalization_rule('error_rate', 0, 1, higher_is_better=False)
        
        # Set default thresholds
        self.set_threshold('pass_rate', 0.7)
        self.set_threshold('pass@1', 0.5)
        
        # Set default weights
        self.set_weight('pass@1', 0.4)
        self.set_weight('pass@5', 0.3)
        self.set_weight('pass_rate', 0.2)
        self.set_weight('error_rate', 0.1)

    def calculate(self, results: List[EvaluationResult]) -> Dict[str, float]:
        """Calculate functional metrics"""
        if not results:
            return {}
        
        metrics = {}
        
        # Overall pass rate
        passed = sum(1 for r in results if r.passed)
        total = len(results)
        metrics['pass_rate'] = passed / total if total > 0 else 0
        
        # Error rate
        errors = sum(len(r.errors) for r in results)
        metrics['error_rate'] = errors / total if total > 0 else 0
        
        # Group by problem and model for Pass@k
        problem_model_groups = defaultdict(list)
        for result in results:
            key = (result.problem_id, result.model_id)
            problem_model_groups[key].append(result)
        
        # Calculate Pass@k for different k values
        for k in [1, 5, 10]:
            pass_at_k = self._calculate_pass_at_k(problem_model_groups, k)
            metrics[f'pass@{k}'] = pass_at_k
        
        return metrics

    def calculate_aggregate_metrics(self, results: List[EvaluationResult]) -> Dict[str, Any]:
        """Calculate aggregate metrics across all results"""
        if not results:
            return {}
        
        metrics = {}
        
        # Basic counts
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        
        metrics['total_results'] = total
        metrics['passed_results'] = passed
        metrics['failed_results'] = total - passed
        metrics['pass_rate'] = passed / total if total > 0 else 0
        
        # Group by problem and model for Pass@k
        problem_model_groups = defaultdict(list)
        for result in results:
            key = (result.problem_id, result.model_id)
            problem_model_groups[key].append(result)
        
        # Calculate Pass@k for different k values
        for k in [1, 5, 10]:
            pass_at_k = self._calculate_pass_at_k(problem_model_groups, k)
            metrics[f'pass@{k}'] = pass_at_k
        
        # Error rate
        error_count = sum(len(r.errors) for r in results)
        metrics['error_rate'] = error_count / total if total > 0 else 0
        metrics['total_errors'] = error_count
        
        # Execution time stats
        exec_times = [r.execution_time_ms for r in results if r.execution_time_ms]
        if exec_times:
            metrics['avg_execution_time_ms'] = sum(exec_times) / len(exec_times)
            metrics['min_execution_time_ms'] = min(exec_times)
            metrics['max_execution_time_ms'] = max(exec_times)
            metrics['total_execution_time_ms'] = sum(exec_times)
        else:
            metrics['avg_execution_time_ms'] = 0
            metrics['min_execution_time_ms'] = 0
            metrics['max_execution_time_ms'] = 0
            metrics['total_execution_time_ms'] = 0
        
        # Test statistics
        total_tests = 0
        passed_tests = 0
        for result in results:
            if hasattr(result, 'test_results') and result.test_results:
                total_tests += len(result.test_results)
                passed_tests += sum(1 for t in result.test_results if t.get('passed', False))
        
        if total_tests > 0:
            metrics['total_tests'] = total_tests
            metrics['passed_tests'] = passed_tests
            metrics['test_pass_rate'] = passed_tests / total_tests
        else:
            metrics['total_tests'] = 0
            metrics['passed_tests'] = 0
            metrics['test_pass_rate'] = 0
        
        # Model-specific metrics
        model_metrics = self.calculate_by_model(results)
        metrics['by_model'] = model_metrics
        
        # Problem-specific metrics
        problem_stats = self.calculate_per_problem_stats(results)
        metrics['by_problem'] = problem_stats
        
        return metrics

    def _calculate_pass_at_k(
        self,
        groups: Dict[tuple, List[EvaluationResult]],
        k: int
    ) -> float:
        """Calculate unbiased Pass@k estimator"""
        pass_rates = []
        
        for (problem_id, model_id), results in groups.items():
            n = len(results)
            if n < k:
                continue
            
            # Count passing samples
            c = sum(1 for r in results if r.passed)
            
            # Unbiased estimator from the Codex paper
            if n - c < k:
                pass_rate = 1.0
            else:
                # Calculate 1 - comb(n-c, k) / comb(n, k)
                # Using product formula for numerical stability
                pass_rate = 1.0
                for i in range(k):
                    pass_rate *= (n - c - i) / (n - i)
                pass_rate = 1.0 - pass_rate
            
            pass_rates.append(pass_rate)
        
        return np.mean(pass_rates) if pass_rates else 0.0

    def calculate_per_problem_stats(
        self,
        results: List[EvaluationResult]
    ) -> Dict[str, Dict[str, float]]:
        """Calculate per-problem statistics"""
        problem_stats = defaultdict(lambda: {
            'total_samples': 0,
            'passed_samples': 0,
            'pass_rate': 0,
            'avg_execution_time': 0,
            'total_tests': 0,
            'passed_tests': 0,
            'test_pass_rate': 0,
            'total_errors': 0
        })
        
        for result in results:
            stats = problem_stats[result.problem_id]
            stats['total_samples'] += 1
            if result.passed:
                stats['passed_samples'] += 1
            
            if result.execution_time_ms:
                stats['avg_execution_time'] += result.execution_time_ms
            
            if result.test_results:
                stats['total_tests'] += len(result.test_results)
                stats['passed_tests'] += sum(1 for t in result.test_results if t.get('passed', False))
            
            stats['total_errors'] += len(result.errors)
        
        # Calculate averages
        for problem_id, stats in problem_stats.items():
            if stats['total_samples'] > 0:
                stats['pass_rate'] = stats['passed_samples'] / stats['total_samples']
                stats['avg_execution_time'] /= stats['total_samples']
            
            if stats['total_tests'] > 0:
                stats['test_pass_rate'] = stats['passed_tests'] / stats['total_tests']
            
            if stats['total_samples'] > 0:
                stats['avg_errors_per_sample'] = stats['total_errors'] / stats['total_samples']
        
        return dict(problem_stats)

    def calculate_by_model(
        self,
        results: List[EvaluationResult]
    ) -> Dict[str, Dict[str, float]]:
        """Calculate metrics grouped by model"""
        model_results = defaultdict(list)
        for result in results:
            model_results[result.model_id].append(result)
        
        model_metrics = {}
        for model_id, model_results_list in model_results.items():
            metrics = self.calculate(model_results_list)
            
            # Add aggregate stats
            total = len(model_results_list)
            passed = sum(1 for r in model_results_list if r.passed)
            
            metrics['total_samples'] = total
            metrics['passed_samples'] = passed
            metrics['failed_samples'] = total - passed
            
            # Execution time
            exec_times = [r.execution_time_ms for r in model_results_list if r.execution_time_ms]
            if exec_times:
                metrics['avg_execution_time_ms'] = sum(exec_times) / len(exec_times)
            
            # Error count
            metrics['total_errors'] = sum(len(r.errors) for r in model_results_list)
            
            model_metrics[model_id] = metrics
        
        return model_metrics

    def get_summary_stats(self, results: List[EvaluationResult]) -> Dict[str, Any]:
        """Get summary statistics for display"""
        if not results:
            return {}
        
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        
        return {
            'total_evaluations': total,
            'passed': passed,
            'failed': total - passed,
            'pass_rate': passed / total if total > 0 else 0,
            'total_errors': sum(len(r.errors) for r in results),
            'avg_execution_time': np.mean([r.execution_time_ms for r in results if r.execution_time_ms]) if any(r.execution_time_ms for r in results) else 0,
            'models_tested': len(set(r.model_id for r in results)),
            'problems_tested': len(set(r.problem_id for r in results))
        }