
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import logging
from datetime import datetime

from ..entities import EvaluationResult, Metric

logger = logging.getLogger(__name__)


class MetricCalculator(ABC):
    """Base class for all metric calculators"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.calculator_id = self._generate_id()
        self.supported_metrics: List[str] = []
        self.normalization_rules: Dict[str, Dict[str, float]] = {}
        self.thresholds: Dict[str, float] = {}
        self.weights: Dict[str, float] = {}
        
        logger.info(f"Initialized {self.__class__.__name__}")

    def _generate_id(self) -> str:
        """Generate a unique calculator ID"""
        import secrets
        return f"calc_{secrets.token_hex(8)}"

    @abstractmethod
    def calculate(self, results: List[EvaluationResult]) -> Dict[str, float]:
        """Calculate metrics from results"""
        pass

    def calculate_for_result(self, result: EvaluationResult) -> Dict[str, float]:
        """Calculate metrics for a single result"""
        return self.calculate([result])

    def normalize(
        self,
        metric_name: str,
        value: float,
        target_range: Tuple[float, float] = (0, 1)
    ) -> float:
        """Normalize a metric value"""
        if metric_name not in self.normalization_rules:
            return value
        
        rules = self.normalization_rules[metric_name]
        min_val = rules.get('min', 0)
        max_val = rules.get('max', 1)
        higher_is_better = rules.get('higher_is_better', True)
        
        # Min-max normalization
        if max_val == min_val:
            normalized = target_range[0]
        else:
            normalized = (value - min_val) / (max_val - min_val)
            normalized = normalized * (target_range[1] - target_range[0]) + target_range[0]
        
        # Invert if lower is better
        if not higher_is_better:
            normalized = target_range[1] - normalized + target_range[0]
        
        return max(target_range[0], min(target_range[1], normalized))

    def compare_metrics(
        self,
        metrics1: Dict[str, float],
        metrics2: Dict[str, float]
    ) -> Dict[str, Any]:
        """Compare two sets of metrics"""
        comparison = {
            'differences': {},
            'better_in': [],
            'worse_in': [],
            'tie_in': [],
            'aggregate_score_diff': 0
        }
        
        all_metrics = set(metrics1.keys()) | set(metrics2.keys())
        
        score1 = 0
        score2 = 0
        
        for metric in all_metrics:
            val1 = metrics1.get(metric, 0)
            val2 = metrics2.get(metric, 0)
            
            diff = val1 - val2
            comparison['differences'][metric] = diff
            
            higher_is_better = self.normalization_rules.get(metric, {}).get('higher_is_better', True)
            
            if abs(diff) < 1e-6:
                comparison['tie_in'].append(metric)
            elif (diff > 0 and higher_is_better) or (diff < 0 and not higher_is_better):
                comparison['better_in'].append(metric)
            else:
                comparison['worse_in'].append(metric)
            
            # Aggregate score
            weight = self.weights.get(metric, 1.0)
            score1 += self.normalize(metric, val1) * weight
            score2 += self.normalize(metric, val2) * weight
        
        comparison['aggregate_score_diff'] = score1 - score2
        
        return comparison

    def calculate_aggregate_score(
        self,
        metrics: Dict[str, float],
        custom_weights: Optional[Dict[str, float]] = None
    ) -> float:
        """Calculate aggregate score from metrics"""
        weights = custom_weights or self.weights
        total_weight = sum(weights.values())
        
        if total_weight == 0:
            return 0.0
        
        score = 0.0
        for metric, value in metrics.items():
            if metric in weights:
                normalized = self.normalize(metric, value)
                score += normalized * weights[metric]
        
        return score / total_weight

    def set_threshold(self, metric_name: str, threshold: float) -> None:
        """Set threshold for a metric"""
        self.thresholds[metric_name] = threshold

    def set_weight(self, metric_name: str, weight: float) -> None:
        """Set weight for a metric"""
        self.weights[metric_name] = weight

    def set_normalization_rule(
        self,
        metric_name: str,
        min_val: float,
        max_val: float,
        higher_is_better: bool = True
    ) -> None:
        """Set normalization rule for a metric"""
        self.normalization_rules[metric_name] = {
            'min': min_val,
            'max': max_val,
            'higher_is_better': higher_is_better
        }

    def get_metric_explanation(self, metric_name: str) -> str:
        """Get explanation for a metric"""
        explanations = {
            'pass_rate': 'Percentage of test cases that passed',
            'pass@1': 'Probability that the first generated solution passes all tests',
            'pass@5': 'Probability that at least one of five generated solutions passes all tests',
            'execution_time': 'Average execution time in milliseconds',
            'memory_usage': 'Peak memory usage in KB',
            'codebleu': 'CodeBERT-based semantic similarity score (0-1)',
            'cyclomatic_complexity': 'Measure of code complexity based on control flow',
            'maintainability_index': 'Measure of how maintainable the code is (0-100)',
            'cognitive_complexity': 'Measure of how difficult code is to understand',
            'error_count': 'Number of errors encountered during execution',
            'syntax_errors': 'Number of syntax errors in generated code',
            'runtime_errors': 'Number of runtime errors during execution'
        }
        return explanations.get(metric_name, f'No explanation available for {metric_name}')