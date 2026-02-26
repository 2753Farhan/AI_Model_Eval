
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import defaultdict, Counter
import re
import ast
import logging
from datetime import datetime, timedelta

from ..entities import Error, EvaluationResult

logger = logging.getLogger(__name__)


class ErrorAnalyzer:
    """Analyzes errors from code execution"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.analyzer_id = self._generate_id()
        self.error_patterns: Dict[str, Dict[str, Any]] = {}
        self.classification_rules: Dict[str, List[str]] = self._init_classification_rules()
        self.fix_suggestions: Dict[str, List[str]] = self._init_fix_suggestions()
        self.error_history: List[Dict[str, Any]] = []
        
        logger.info(f"Initialized ErrorAnalyzer with {len(self.classification_rules)} rules")

    def _generate_id(self) -> str:
        """Generate a unique analyzer ID"""
        import secrets
        return f"analyzer_{secrets.token_hex(8)}"

    def _init_classification_rules(self) -> Dict[str, List[str]]:
        """Initialize error classification rules"""
        return {
            'syntax_error': [
                'invalid syntax',
                'unexpected EOF',
                'expected',
                'missing',
                'unmatched',
                'IndentationError',
                'TabError'
            ],
            'name_error': [
                'is not defined',
                'NameError',
                'undefined name'
            ],
            'type_error': [
                'TypeError',
                'unsupported operand type',
                'must be',
                'cannot be'
            ],
            'value_error': [
                'ValueError',
                'invalid literal',
                'could not convert'
            ],
            'attribute_error': [
                'AttributeError',
                'has no attribute'
            ],
            'index_error': [
                'IndexError',
                'list index out of range'
            ],
            'key_error': [
                'KeyError'
            ],
            'zero_division_error': [
                'division by zero',
                'ZeroDivisionError'
            ],
            'import_error': [
                'ImportError',
                'ModuleNotFoundError',
                'No module named'
            ],
            'runtime_error': [
                'RuntimeError',
                'maximum recursion depth exceeded',
                'TimeoutError'
            ],
            'assertion_error': [
                'AssertionError',
                'assert'
            ],
            'memory_error': [
                'MemoryError',
                'out of memory',
                'cannot allocate'
            ],
            'timeout_error': [
                'Timeout',
                'timed out',
                'execution time exceeded'
            ]
        }

    def _init_fix_suggestions(self) -> Dict[str, List[str]]:
        """Initialize fix suggestions for common errors"""
        return {
            'syntax_error': [
                "Check for missing parentheses, brackets, or quotes",
                "Ensure proper indentation (use spaces consistently)",
                "Verify that all strings are properly closed",
                "Check for missing colons after if/for/while statements"
            ],
            'name_error': [
                "Check if the variable/function is defined before use",
                "Verify spelling of variable/function names",
                "Ensure proper import of required modules",
                "Check scope of variable (local vs global)"
            ],
            'type_error': [
                "Verify that operands have compatible types",
                "Check if variable is None before using it",
                "Ensure function arguments are of correct type",
                "Convert types explicitly if needed (str(), int(), etc.)"
            ],
            'value_error': [
                "Check if input values are within expected range",
                "Verify that strings can be converted to numbers",
                "Ensure list indices are integers, not floats",
                "Check for empty sequences in operations"
            ],
            'attribute_error': [
                "Verify that the object has the required attribute/method",
                "Check if you're using the correct object type",
                "Ensure module imports are correct",
                "Check for typos in attribute names"
            ],
            'index_error': [
                "Verify that list indices are within bounds",
                "Check if list is empty before accessing elements",
                "Use len() to check list size before indexing",
                "Consider using try-except for safe access"
            ],
            'key_error': [
                "Check if dictionary key exists before accessing",
                "Use dict.get() for safe access with default value",
                "Verify dictionary contents",
                "Consider using defaultdict for missing keys"
            ],
            'zero_division_error': [
                "Check if denominator is zero before division",
                "Add a condition to handle zero case",
                "Use try-except to catch division by zero",
                "Ensure values are not zero in calculations"
            ],
            'import_error': [
                "Install required module using pip",
                "Check module name spelling",
                "Verify virtual environment is activated",
                "Check if module is in Python path"
            ],
            'memory_error': [
                "Reduce data size or process in chunks",
                "Use generators instead of lists for large data",
                "Free unused memory with del and gc.collect()",
                "Consider using more efficient algorithms"
            ],
            'timeout_error': [
                "Optimize code for better performance",
                "Reduce input size or complexity",
                "Use caching for repeated calculations",
                "Consider iterative instead of recursive solutions"
            ]
        }

    def analyze_error(self, error: Error) -> Dict[str, Any]:
        """Analyze a single error"""
        analysis = {
            'error_id': error.error_id,
            'error_type': error.error_type,
            'error_message': error.error_message,
            'classification': self.classify_error(error),
            'suggestions': self.suggest_fix(error),
            'pattern': self.find_similar_errors(error),
            'severity': self.calculate_severity(error),
            'frequency': error.frequency
        }
        
        return analysis

    def classify_error(self, error: Error) -> str:
        """Classify error type"""
        error_msg = error.error_message.lower()
        
        for error_type, patterns in self.classification_rules.items():
            for pattern in patterns:
                if pattern.lower() in error_msg:
                    return error_type
        
        # Default to original error type if no match
        return error.error_type

    def suggest_fix(self, error: Error) -> List[str]:
        """Suggest fixes for error"""
        error_type = self.classify_error(error)
        
        # Get general suggestions for this error type
        suggestions = self.fix_suggestions.get(error_type, [
            "Review the error message and check the code around the reported line",
            "Use print statements to debug variable values",
            "Consider using a debugger to step through the code"
        ])
        
        # Add specific suggestions based on error message
        error_msg = error.error_message.lower()
        
        if 'indentation' in error_msg:
            suggestions.insert(0, "Check that all code blocks are properly indented with consistent spaces/tabs")
        
        if 'expected an indented block' in error_msg:
            suggestions.insert(0, "Add proper indentation after function definitions, if/else, for/while loops")
        
        if 'unexpected indent' in error_msg:
            suggestions.insert(0, "Remove extra indentation or check for mixed tabs and spaces")
        
        if 'is not defined' in error_msg:
            # Extract variable name
            import re
            match = re.search(r"'(\w+)' is not defined", error_msg)
            if match:
                var_name = match.group(1)
                suggestions.insert(0, f"Check if '{var_name}' is defined before use, or if there's a typo")
        
        return suggestions

    def find_similar_errors(
        self,
        error: Error,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Find similar errors from history"""
        if not self.error_history:
            return []
        
        similar = []
        error_signature = self._get_error_signature(error)
        
        for hist_error in self.error_history[-100:]:  # Check last 100 errors
            hist_signature = self._get_error_signature(hist_error)
            
            if error_signature == hist_signature:
                similar.append(hist_error)
                if len(similar) >= max_results:
                    break
        
        return similar

    def _get_error_signature(self, error: Dict[str, Any]) -> str:
        """Get error signature for matching"""
        # Normalize error message by removing variable parts
        msg = error.get('error_message', '')
        
        # Remove line numbers
        msg = re.sub(r'line \d+', 'line N', msg)
        
        # Remove quoted strings
        msg = re.sub(r'"[^"]*"', '"..."', msg)
        msg = re.sub(r"'[^']*'", "'...'", msg)
        
        # Remove numbers
        msg = re.sub(r'\b\d+\b', 'N', msg)
        
        return f"{error.get('error_type', 'unknown')}:{msg[:100]}"

    def calculate_severity(self, error: Error) -> str:
        """Calculate error severity"""
        error_type = error.error_type
        error_msg = error.error_message.lower()
        
        # Critical errors
        if error_type in ['memory_error', 'timeout_error']:
            return 'critical'
        
        if 'out of memory' in error_msg or 'cannot allocate' in error_msg:
            return 'critical'
        
        # High severity
        if error_type in ['runtime_error', 'zero_division_error']:
            return 'high'
        
        if 'maximum recursion depth exceeded' in error_msg:
            return 'high'
        
        # Medium severity
        if error_type in ['syntax_error', 'type_error', 'name_error', 'attribute_error']:
            return 'medium'
        
        # Low severity
        if error_type in ['assertion_error', 'value_error', 'index_error', 'key_error']:
            return 'low'
        
        return 'unknown'

    def analyze_errors(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze multiple errors"""
        if not errors:
            return {
                'total_errors': 0,
                'unique_errors': 0,
                'by_type': {},
                'by_severity': {},
                'most_common': [],
                'patterns': {}
            }
        
        # Add to history
        self.error_history.extend(errors)
        
        # Group by type
        by_type = defaultdict(int)
        by_severity = defaultdict(int)
        error_messages = []
        
        for error in errors:
            error_type = error.get('error_type', 'unknown')
            severity = self.calculate_severity(Error.from_dict(error))
            
            by_type[error_type] += 1
            by_severity[severity] += 1
            error_messages.append(error.get('error_message', ''))
        
        # Find most common error messages
        msg_counter = Counter(error_messages)
        most_common = [
            {'message': msg, 'count': count}
            for msg, count in msg_counter.most_common(5)
        ]
        
        # Detect patterns
        patterns = self.detect_patterns(errors)
        
        return {
            'total_errors': len(errors),
            'unique_errors': len(set(e.get('error_message', '') for e in errors)),
            'by_type': dict(by_type),
            'by_severity': dict(by_severity),
            'most_common': most_common,
            'patterns': patterns
        }

    def detect_patterns(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect error patterns"""
        patterns = {}
        
        # Group errors by type
        type_groups = defaultdict(list)
        for error in errors:
            error_type = error.get('error_type', 'unknown')
            type_groups[error_type].append(error)
        
        for error_type, type_errors in type_groups.items():
            if len(type_errors) < 3:
                continue
            
            # Look for common patterns in messages
            messages = [e.get('error_message', '') for e in type_errors]
            
            # Find common substrings
            common = self._find_common_substrings(messages)
            
            if common:
                patterns[error_type] = {
                    'count': len(type_errors),
                    'common_patterns': common,
                    'suggestions': self.fix_suggestions.get(error_type, [])
                }
        
        return patterns

    def _find_common_substrings(self, strings: List[str], min_length: int = 10) -> List[str]:
        """Find common substrings in error messages"""
        if len(strings) < 2:
            return []
        
        common = []
        
        # Find longest common substring between first two
        s1, s2 = strings[0], strings[1]
        
        # Simple LCS implementation
        matrix = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
        longest = 0
        longest_str = ""
        
        for i in range(len(s1)):
            for j in range(len(s2)):
                if s1[i] == s2[j]:
                    matrix[i+1][j+1] = matrix[i][j] + 1
                    if matrix[i+1][j+1] > longest:
                        longest = matrix[i+1][j+1]
                        longest_str = s1[i-longest+1:i+1]
                else:
                    matrix[i+1][j+1] = 0
        
        if len(longest_str) >= min_length:
            common.append(longest_str)
        
        return common

    def generate_error_report(
        self,
        errors: List[Dict[str, Any]],
        format: str = 'summary'
    ) -> Dict[str, Any]:
        """Generate error analysis report"""
        analysis = self.analyze_errors(errors)
        
        if format == 'summary':
            return {
                'total_errors': analysis['total_errors'],
                'error_rate': analysis['total_errors'] / max(len(errors), 1),
                'most_common_type': max(analysis['by_type'].items(), key=lambda x: x[1])[0] if analysis['by_type'] else None,
                'critical_errors': analysis['by_severity'].get('critical', 0),
                'suggestions': self._get_general_suggestions(analysis)
            }
        
        return analysis

    def _get_general_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """Get general suggestions based on error analysis"""
        suggestions = []
        
        if analysis['by_severity'].get('critical', 0) > 0:
            suggestions.append("Critical errors detected. Check system resources and timeout settings.")
        
        if analysis['by_type'].get('syntax_error', 0) > analysis['total_errors'] * 0.3:
            suggestions.append("High number of syntax errors. Consider using a linter or IDE with syntax checking.")
        
        if analysis['by_type'].get('name_error', 0) > analysis['total_errors'] * 0.2:
            suggestions.append("Many name errors. Review variable scope and naming conventions.")
        
        if analysis['by_type'].get('type_error', 0) > analysis['total_errors'] * 0.2:
            suggestions.append("Frequent type errors. Add type checking or use type hints.")
        
        return suggestions