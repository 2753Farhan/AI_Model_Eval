
from typing import List, Dict, Any, Optional
import ast
import radon
from radon.raw import analyze
from radon.complexity import cc_visit
from radon.metrics import mi_visit
import logging

from .metric_calculator import MetricCalculator
from ..entities import EvaluationResult, Metric

logger = logging.getLogger(__name__)


class QualityMetricsCalculator(MetricCalculator):
    """Calculator for code quality metrics"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.supported_metrics = [
            'loc', 'lloc', 'comments', 'cyclomatic_complexity',
            'maintainability_index', 'cognitive_complexity'
        ]
        
        # Set normalization rules
        self.set_normalization_rule('loc', 0, 100, higher_is_better=False)
        self.set_normalization_rule('cyclomatic_complexity', 0, 20, higher_is_better=False)
        self.set_normalization_rule('maintainability_index', 0, 100, higher_is_better=True)
        self.set_normalization_rule('cognitive_complexity', 0, 50, higher_is_better=False)
        
        # Set default thresholds
        self.set_threshold('maintainability_index', 60)
        self.set_threshold('cyclomatic_complexity', 10)
        
        # Set default weights
        self.set_weight('maintainability_index', 0.4)
        self.set_weight('cyclomatic_complexity', 0.3)
        self.set_weight('cognitive_complexity', 0.2)
        self.set_weight('loc', 0.1)

    def calculate(self, results: List[EvaluationResult]) -> Dict[str, float]:
        """Calculate quality metrics"""
        if not results:
            return {}
        
        metrics = {}
        
        # Collect all code
        all_code = [r.generated_code for r in results if r.generated_code]
        
        if not all_code:
            return {}
        
        # Calculate average metrics across all code
        total_loc = 0
        total_lloc = 0
        total_comments = 0
        total_complexity = 0
        total_maintainability = 0
        total_cognitive = 0
        count = 0
        
        for code in all_code:
            try:
                # Radon metrics
                raw = analyze(code)
                total_loc += raw.loc
                total_lloc += raw.lloc
                total_comments += raw.comments
                
                # Cyclomatic complexity
                cc_metrics = cc_visit(code)
                if cc_metrics:
                    avg_cc = sum(c.complexity for c in cc_metrics) / len(cc_metrics)
                    total_complexity += avg_cc
                
                # Maintainability index
                mi = mi_visit(code, multi=True)
                total_maintainability += mi
                
                # Cognitive complexity
                cognitive = self._calculate_cognitive_complexity(code)
                total_cognitive += cognitive
                
                count += 1
                
            except Exception as e:
                logger.debug(f"Failed to analyze code quality: {e}")
        
        if count > 0:
            metrics['loc'] = total_loc / count
            metrics['lloc'] = total_lloc / count
            metrics['comments'] = total_comments / count
            metrics['cyclomatic_complexity'] = total_complexity / count
            metrics['maintainability_index'] = total_maintainability / count
            metrics['cognitive_complexity'] = total_cognitive / count
        
        return metrics

    def _calculate_cognitive_complexity(self, code: str) -> float:
        """Calculate cognitive complexity"""
        try:
            score = 0
            lines = code.split('\n')
            nesting_level = 0
            
            control_keywords = [
                'if ', 'elif ', 'else:', 'for ', 'while ',
                'except ', 'try:', 'with ', 'case ', 'default:'
            ]
            
            for line in lines:
                stripped = line.strip()
                
                # Skip comments and empty lines
                if stripped.startswith('#') or not stripped:
                    continue
                
                # Check for control flow keywords
                for keyword in control_keywords:
                    if keyword in stripped:
                        score += 1 + nesting_level
                        break
                
                # Track nesting level
                if stripped.endswith(':'):
                    nesting_level += 1
                elif nesting_level > 0 and len(stripped) > 0 and len(stripped) - len(stripped.lstrip()) == 0:
                    nesting_level = max(0, nesting_level - 1)
            
            return max(0, score)
            
        except Exception:
            return 0

    def calculate_per_file(self, code: str) -> Dict[str, float]:
        """Calculate quality metrics for a single file"""
        metrics = {}
        
        try:
            # Radon metrics
            raw = analyze(code)
            metrics['loc'] = raw.loc
            metrics['lloc'] = raw.lloc
            metrics['comments'] = raw.comments
            
            # Cyclomatic complexity
            cc_metrics = cc_visit(code)
            if cc_metrics:
                metrics['cyclomatic_complexity'] = sum(c.complexity for c in cc_metrics) / len(cc_metrics)
                metrics['total_complexity'] = sum(c.complexity for c in cc_metrics)
                metrics['function_count'] = len(cc_metrics)
            else:
                metrics['cyclomatic_complexity'] = 0
                metrics['function_count'] = 0
            
            # Maintainability index
            metrics['maintainability_index'] = mi_visit(code, multi=True)
            
            # Cognitive complexity
            metrics['cognitive_complexity'] = self._calculate_cognitive_complexity(code)
            
        except Exception as e:
            logger.error(f"Failed to calculate quality metrics: {e}")
        
        return metrics

    def grade_quality(self, metrics: Dict[str, float]) -> str:
        """Grade code quality based on metrics"""
        if 'maintainability_index' in metrics:
            mi = metrics['maintainability_index']
            if mi >= 80:
                return 'Excellent'
            elif mi >= 60:
                return 'Good'
            elif mi >= 40:
                return 'Fair'
            else:
                return 'Poor'
        
        if 'cyclomatic_complexity' in metrics:
            cc = metrics['cyclomatic_complexity']
            if cc <= 5:
                return 'Excellent'
            elif cc <= 10:
                return 'Good'
            elif cc <= 15:
                return 'Fair'
            else:
                return 'Poor'
        
        return 'Unknown'