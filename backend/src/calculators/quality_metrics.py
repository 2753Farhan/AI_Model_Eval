# src/calculators/quality_metrics.py

from typing import List, Dict, Any, Optional
import ast
import radon
from radon.raw import analyze
from radon.complexity import cc_visit
from radon.metrics import mi_visit
import logging
import re

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
                # Fix code indentation first
                fixed_code = self._fix_code_indentation(code)
                
                # Radon metrics
                raw = analyze(fixed_code)
                total_loc += raw.loc
                total_lloc += raw.lloc
                total_comments += raw.comments
                
                # Cyclomatic complexity
                cc_metrics = cc_visit(fixed_code)
                if cc_metrics:
                    avg_cc = sum(c.complexity for c in cc_metrics) / len(cc_metrics)
                    total_complexity += avg_cc
                
                # Maintainability index
                mi = mi_visit(fixed_code, multi=True)
                total_maintainability += mi
                
                # Cognitive complexity
                cognitive = self._calculate_cognitive_complexity(fixed_code)
                total_cognitive += cognitive
                
                count += 1
                
            except Exception as e:
                logger.debug(f"Failed to analyze code quality: {e}")
                # Still try to count basic metrics
                try:
                    lines = code.split('\n')
                    total_loc += len(lines)
                    total_lloc += sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
                    total_comments += sum(1 for line in lines if line.strip().startswith('#'))
                    count += 1
                except:
                    pass
        
        if count > 0:
            metrics['loc'] = total_loc / count
            metrics['lloc'] = total_lloc / count
            metrics['comments'] = total_comments / count
            metrics['cyclomatic_complexity'] = total_complexity / count if total_complexity > 0 else 0
            metrics['maintainability_index'] = total_maintainability / count if total_maintainability > 0 else 50
            metrics['cognitive_complexity'] = total_cognitive / count if total_cognitive > 0 else 0
        
        return metrics

    def _calculate_cognitive_complexity(self, code: str) -> float:
        """Calculate cognitive complexity"""
        try:
            score = 0
            lines = code.split('\n')
            nesting_level = 0
            
            control_keywords = [
                'if ', 'elif ', 'else:', 'for ', 'while ',
                'except ', 'try:', 'with ', 'case ', 'default:',
                'and ', 'or ', 'not ', 'in ', 'is ', 'is not'
            ]
            
            for line in lines:
                stripped = line.strip()
                
                # Skip comments and empty lines
                if stripped.startswith('#') or not stripped:
                    continue
                
                # Check for control flow keywords
                for keyword in control_keywords:
                    if keyword in stripped:
                        # Add base score + nesting bonus
                        score += 1 + nesting_level
                        break
                
                # Track nesting level based on indentation
                if stripped.endswith(':'):
                    nesting_level += 1
                elif nesting_level > 0:
                    # Check if indentation decreased
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent == 0:
                        nesting_level = max(0, nesting_level - 1)
            
            return max(0, score)
            
        except Exception as e:
            logger.debug(f"Cognitive complexity calculation failed: {e}")
            return 0

    def calculate_per_file(self, code: str) -> Dict[str, float]:
        """Calculate quality metrics for a single file"""
        metrics = {}
        
        if not code or not isinstance(code, str):
            return metrics
        
        try:
            # First, try to fix common indentation issues
            fixed_code = self._fix_code_indentation(code)
            
            # Basic metrics (these don't need parsing)
            lines = fixed_code.split('\n')
            metrics['loc'] = len(lines)
            metrics['blank_lines'] = sum(1 for line in lines if not line.strip())
            metrics['code_lines'] = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
            metrics['comment_lines'] = sum(1 for line in lines if line.strip().startswith('#'))
            
            # Count function definitions
            metrics['function_count'] = fixed_code.count('def ')
            metrics['class_count'] = fixed_code.count('class ')
            
            # Try to parse the code for advanced metrics
            try:
                # Cyclomatic complexity
                cc_metrics = cc_visit(fixed_code)
                if cc_metrics:
                    metrics['cyclomatic_complexity'] = sum(c.complexity for c in cc_metrics) / len(cc_metrics)
                    metrics['total_complexity'] = sum(c.complexity for c in cc_metrics)
                    metrics['function_count'] = len(cc_metrics)
                else:
                    metrics['cyclomatic_complexity'] = 0
                
                # Maintainability index
                metrics['maintainability_index'] = mi_visit(fixed_code, multi=True)
                
                # Raw metrics from radon
                raw = analyze(fixed_code)
                metrics['lloc'] = raw.lloc
                metrics['sloc'] = raw.sloc
                metrics['comments'] = raw.comments
                metrics['multi'] = raw.multi
                metrics['blank'] = raw.blank
                
            except Exception as e:
                logger.debug(f"Failed to calculate advanced metrics: {e}")
                # Fallback values
                metrics['cyclomatic_complexity'] = 0
                metrics['maintainability_index'] = 50  # Default middle value
                metrics['lloc'] = metrics['code_lines']
                metrics['sloc'] = metrics['code_lines']
            
            # Cognitive complexity (our own calculation)
            metrics['cognitive_complexity'] = self._calculate_cognitive_complexity(fixed_code)
            
            # Calculate derived metrics
            if metrics['code_lines'] > 0:
                metrics['comment_density'] = metrics.get('comments', 0) / metrics['code_lines']
            else:
                metrics['comment_density'] = 0
            
            if metrics['function_count'] > 0 and metrics['cyclomatic_complexity'] > 0:
                metrics['avg_complexity_per_function'] = metrics['cyclomatic_complexity']
            
        except Exception as e:
            logger.error(f"Failed to calculate quality metrics: {e}")
            # Return basic metrics at least
            if code:
                lines = code.split('\n')
                metrics['loc'] = len(lines)
                metrics['code_lines'] = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
                metrics['function_count'] = code.count('def ')
                metrics['class_count'] = code.count('class ')
                metrics['cyclomatic_complexity'] = 0
                metrics['maintainability_index'] = 50
        
        return metrics

    def _fix_code_indentation(self, code: str) -> str:
        """Fix common indentation issues in code"""
        if not code:
            return ""
        
        lines = code.split('\n')
        fixed_lines = []
        
        # Track indentation level
        current_indent = 0
        indent_size = 4  # Assume 4 spaces
        in_multiline_string = False
        multiline_delimiter = None
        
        # First pass: normalize line endings and remove mixed whitespace
        normalized_lines = []
        for line in lines:
            # Replace tabs with spaces
            line = line.replace('\t', '    ')
            # Remove trailing whitespace
            line = line.rstrip()
            normalized_lines.append(line)
        
        i = 0
        while i < len(normalized_lines):
            line = normalized_lines[i]
            stripped = line.strip()
            
            # Handle empty lines
            if not stripped:
                fixed_lines.append('')
                i += 1
                continue
            
            # Handle multiline strings
            if not in_multiline_string:
                # Check for start of multiline string
                if '"""' in line or "'''" in line:
                    # Count occurrences to handle both start and end in same line
                    triple_quotes = line.count('"""') + line.count("'''")
                    if triple_quotes % 2 == 1:
                        in_multiline_string = True
                        # Find which delimiter was used
                        if '"""' in line:
                            multiline_delimiter = '"""'
                        else:
                            multiline_delimiter = "'''"
            
            # Fix indentation
            if not in_multiline_string:
                # Check if this line should decrease indentation
                if stripped in ['}', ')', ']'] or stripped.startswith(('}', ')', ']')):
                    current_indent = max(0, current_indent - indent_size)
                
                # Apply current indentation
                if current_indent > 0:
                    fixed_lines.append(' ' * current_indent + stripped)
                else:
                    fixed_lines.append(stripped)
                
                # Check if this line should increase indentation
                if stripped.endswith(':'):
                    current_indent += indent_size
                elif stripped.endswith('{') or stripped.endswith('(') or stripped.endswith('['):
                    current_indent += indent_size
            else:
                # In multiline string, preserve original indentation but normalize
                fixed_lines.append(line)
            
            # Handle end of multiline string
            if in_multiline_string and multiline_delimiter in line:
                # Check if this line ends the multiline string
                if line.strip().endswith(multiline_delimiter):
                    in_multiline_string = False
                    multiline_delimiter = None
            
            i += 1
        
        return '\n'.join(fixed_lines)

    def grade_quality(self, metrics: Dict[str, float]) -> str:
        """Grade code quality based on metrics"""
        if not metrics:
            return 'Unknown'
        
        # Try maintainability index first (most comprehensive)
        if 'maintainability_index' in metrics:
            mi = metrics['maintainability_index']
            if mi >= 80:
                return 'A (Excellent)'
            elif mi >= 60:
                return 'B (Good)'
            elif mi >= 40:
                return 'C (Fair)'
            elif mi >= 20:
                return 'D (Poor)'
            else:
                return 'F (Very Poor)'
        
        # Fallback to cyclomatic complexity
        if 'cyclomatic_complexity' in metrics:
            cc = metrics['cyclomatic_complexity']
            if cc <= 5:
                return 'A (Excellent)'
            elif cc <= 10:
                return 'B (Good)'
            elif cc <= 15:
                return 'C (Fair)'
            elif cc <= 20:
                return 'D (Poor)'
            else:
                return 'F (Very Poor)'
        
        # Fallback to function count and size
        if metrics.get('function_count', 0) > 0:
            code_per_function = metrics.get('code_lines', 0) / metrics['function_count']
            if code_per_function <= 10:
                return 'B (Good)'
            elif code_per_function <= 20:
                return 'C (Fair)'
            else:
                return 'D (Poor)'
        
        return 'Unknown'

    def get_quality_score(self, metrics: Dict[str, float]) -> float:
        """Get normalized quality score (0-100)"""
        grade = self.grade_quality(metrics)
        
        # Convert grade to score
        grade_scores = {
            'A (Excellent)': 90,
            'B (Good)': 75,
            'C (Fair)': 60,
            'D (Poor)': 40,
            'F (Very Poor)': 20,
            'Unknown': 50
        }
        
        return grade_scores.get(grade, 50)

    def compare_quality(self, metrics1: Dict[str, float], metrics2: Dict[str, float]) -> Dict[str, Any]:
        """Compare quality between two code samples"""
        score1 = self.get_quality_score(metrics1)
        score2 = self.get_quality_score(metrics2)
        
        differences = {}
        for key in set(metrics1.keys()) | set(metrics2.keys()):
            if key in metrics1 and key in metrics2:
                if isinstance(metrics1[key], (int, float)) and isinstance(metrics2[key], (int, float)):
                    differences[key] = metrics2[key] - metrics1[key]
        
        return {
            'score1': score1,
            'score2': score2,
            'difference': score2 - score1,
            'better': 'code1' if score1 > score2 else 'code2' if score2 > score1 else 'equal',
            'grade1': self.grade_quality(metrics1),
            'grade2': self.grade_quality(metrics2),
            'differences': differences
        }

    def calculate_batch(self, codes: List[str]) -> List[Dict[str, float]]:
        """Calculate metrics for multiple code samples"""
        results = []
        for code in codes:
            results.append(self.calculate_per_file(code))
        return results

    def get_metric_explanation(self, metric_name: str) -> Dict[str, Any]:
        """Get explanation for a specific metric"""
        explanations = {
            'loc': {
                'name': 'Lines of Code',
                'description': 'Total number of lines in the code file, including blank lines and comments.',
                'range': 'Any positive integer',
                'interpretation': 'Lower is generally better, but very low might indicate insufficient functionality'
            },
            'lloc': {
                'name': 'Logical Lines of Code',
                'description': 'Number of executable statements, excluding comments and blank lines.',
                'range': 'Any positive integer',
                'interpretation': 'Lower is better for maintainability'
            },
            'comments': {
                'name': 'Comment Lines',
                'description': 'Number of lines containing comments.',
                'range': 'Any positive integer',
                'interpretation': 'Should be proportional to code complexity'
            },
            'cyclomatic_complexity': {
                'name': 'Cyclomatic Complexity',
                'description': 'Measures the number of linearly independent paths through the code.',
                'range': '1-50+',
                'thresholds': {
                    'excellent': '1-5',
                    'good': '6-10',
                    'fair': '11-15',
                    'poor': '16-20',
                    'very_poor': '21+'
                },
                'interpretation': 'Lower is better. High complexity indicates hard-to-test code.'
            },
            'maintainability_index': {
                'name': 'Maintainability Index',
                'description': 'Combined metric measuring how maintainable the code is.',
                'range': '0-100',
                'thresholds': {
                    'excellent': '80-100',
                    'good': '60-79',
                    'fair': '40-59',
                    'poor': '20-39',
                    'very_poor': '0-19'
                },
                'interpretation': 'Higher is better. Considers code volume, complexity, and comments.'
            },
            'cognitive_complexity': {
                'name': 'Cognitive Complexity',
                'description': 'Measures how hard the code is to understand for humans.',
                'range': '0-50+',
                'thresholds': {
                    'excellent': '0-5',
                    'good': '6-10',
                    'fair': '11-15',
                    'poor': '16-20',
                    'very_poor': '21+'
                },
                'interpretation': 'Lower is better. Accounts for nesting and control flow structures.'
            },
            'comment_density': {
                'name': 'Comment Density',
                'description': 'Ratio of comment lines to code lines.',
                'range': '0-1+',
                'thresholds': {
                    'excellent': '0.2-0.3',
                    'good': '0.1-0.2',
                    'fair': '0.05-0.1',
                    'poor': '<0.05'
                },
                'interpretation': 'Higher indicates well-documented code, but too high may indicate over-commenting.'
            }
        }
        
        return explanations.get(metric_name, {
            'name': metric_name.replace('_', ' ').title(),
            'description': f'Metric: {metric_name}',
            'range': 'Unknown',
            'interpretation': 'No interpretation available'
        })