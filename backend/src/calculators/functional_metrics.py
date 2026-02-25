
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
            'passed_tests': 0
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
        
        # Calculate averages
        for problem_id, stats in problem_stats.items():
            if stats['total_samples'] > 0:
                stats['pass_rate'] = stats['passed_samples'] / stats['total_samples']
                stats['avg_execution_time'] /= stats['total_samples']
            
            if stats['total_tests'] > 0:
                stats['test_pass_rate'] = stats['passed_tests'] / stats['total_tests']
        
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
            model_metrics[model_id] = self.calculate(model_results_list)
        
        return model_metrics