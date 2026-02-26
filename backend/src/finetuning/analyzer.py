# src/finetuning/analyzer.py
"""
Analyzes evaluation results to identify failure patterns for fine-tuning
Uses existing ErrorAnalyzer and PatternDetector
"""

from typing import List, Dict, Any, Optional
from collections import defaultdict
import logging

from ..analyzers import ErrorAnalyzer, PatternDetector
from ..entities import EvaluationResult, Error

logger = logging.getLogger(__name__)

class FailureAnalyzer:
    """Analyzes evaluation failures to identify patterns for fine-tuning"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        # Use existing analyzers
        self.error_analyzer = ErrorAnalyzer(config)
        self.pattern_detector = PatternDetector(config)
        
    def analyze_evaluation(self, results: List[EvaluationResult]) -> Dict[str, Any]:
        """Analyze evaluation results to identify failure patterns"""
        
        # Extract errors from results
        all_errors = []
        failures = []
        
        for result in results:
            if not result.passed:
                failures.append(result)
                # Convert result errors to Error objects if needed
                for err_dict in result.errors:
                    error = Error.from_dict(err_dict) if isinstance(err_dict, dict) else err_dict
                    all_errors.append(error)
        
        # Use existing error analyzer
        error_analysis = self.error_analyzer.analyze_errors([e.to_dict() for e in all_errors])
        
        # Use existing pattern detector
        patterns = self.pattern_detector.detect_patterns([e.to_dict() for e in all_errors])
        
        # Calculate failure statistics
        analysis = {
            'total_problems': len(results),
            'total_failures': len(failures),
            'failure_rate': len(failures) / len(results) if results else 0,
            'error_analysis': error_analysis,
            'patterns': patterns,
            'recommendations': [],
            'target_areas': []
        }
        
        # Generate recommendations based on error analysis
        analysis['recommendations'] = self._generate_recommendations(error_analysis, patterns)
        
        # Identify target areas for fine-tuning
        analysis['target_areas'] = self._identify_target_areas(error_analysis, patterns)
        
        return analysis
    
    def _generate_recommendations(self, error_analysis: Dict, patterns: List) -> List[str]:
        """Generate fine-tuning recommendations"""
        recommendations = []
        
        # Check failure rate
        if error_analysis.get('total_errors', 0) > 50:
            recommendations.append("High error rate detected. Consider comprehensive fine-tuning.")
        
        # Check error types
        by_type = error_analysis.get('by_type', {})
        for error_type, count in by_type.items():
            if count > 10:
                recommendations.append(
                    f"Frequent {error_type} errors ({count} occurrences). "
                    f"Add training examples focusing on {error_type.replace('_', ' ')}."
                )
        
        # Check patterns
        if patterns:
            top_pattern = patterns[0] if patterns else None
            if top_pattern and top_pattern.get('occurrences', 0) > 5:
                recommendations.append(
                    f"Pattern detected: {top_pattern.get('pattern', 'unknown')}. "
                    f"Consider adding similar examples to training data."
                )
        
        return recommendations
    
    def _identify_target_areas(self, error_analysis: Dict, patterns: List) -> List[Dict]:
        """Identify specific areas to target for fine-tuning"""
        target_areas = []
        
        # Target top error types
        by_type = error_analysis.get('by_type', {})
        sorted_types = sorted(by_type.items(), key=lambda x: x[1], reverse=True)
        
        for error_type, count in sorted_types[:3]:  # Top 3 error types
            target_areas.append({
                'type': 'error_category',
                'name': error_type,
                'count': count,
                'priority': 'high' if count > 20 else 'medium'
            })
        
        # Target patterns
        for pattern in patterns[:2]:  # Top 2 patterns
            target_areas.append({
                'type': 'pattern',
                'name': pattern.get('pattern', 'unknown')[:50],
                'count': pattern.get('occurrences', 0),
                'severity': pattern.get('severity', 'medium')
            })
        
        return target_areas
