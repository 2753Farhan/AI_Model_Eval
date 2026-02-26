
from typing import List, Dict, Any, Optional
import ast
import logging
from collections import defaultdict

from ..entities import Error

logger = logging.getLogger(__name__)


class FixSuggester:
    """Suggests fixes for code errors"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.fix_templates: Dict[str, List[Dict[str, Any]]] = self._init_fix_templates()
        self.learning_enabled = config.get('learning_enabled', True)
        self.successful_fixes: List[Dict[str, Any]] = []

    def _init_fix_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize fix templates for common errors"""
        return {
            'syntax_error': [
                {
                    'pattern': r'missing (\w+)',
                    'fix': 'Add missing {0}',
                    'example': 'Missing parenthesis → Add closing parenthesis )'
                },
                {
                    'pattern': r'unexpected indent',
                    'fix': 'Remove extra indentation or check for mixed tabs/spaces',
                    'example': 'Use consistent indentation (4 spaces recommended)'
                }
            ],
            'name_error': [
                {
                    'pattern': r"'(\w+)' is not defined",
                    'fix': "Define '{0}' before use or check for typos",
                    'example': "name 'x' is not defined → x = value before using it"
                }
            ],
            'type_error': [
                {
                    'pattern': r"unsupported operand type\(s\) for ([+-/*]): '(\w+)' and '(\w+)'",
                    'fix': "Convert {1} or {2} to compatible types before operation",
                    'example': "unsupported operand type(s) for +: 'int' and 'str' → Convert str to int: int(str_value)"
                },
                {
                    'pattern': r"'(\w+)' object is not callable",
                    'fix': "Remove parentheses or check if {0} is a function",
                    'example': "'str' object is not callable → Don't use str() as a function call"
                }
            ],
            'value_error': [
                {
                    'pattern': r"invalid literal for int\(\) with base 10: '(\w+)'",
                    'fix': "Ensure string '{0}' contains only digits",
                    'example': "invalid literal for int() with base 10: 'abc' → Check input contains numbers only"
                }
            ],
            'attribute_error': [
                {
                    'pattern': r"'(\w+)' object has no attribute '(\w+)'",
                    'fix': "Check if '{1}' is a valid attribute/method for {0} objects",
                    'example': "'list' object has no attribute 'push' → Use append() instead of push()"
                }
            ],
            'index_error': [
                {
                    'pattern': r'list index out of range',
                    'fix': "Check list length before accessing index, or use try-except",
                    'example': "if i < len(my_list): value = my_list[i]"
                }
            ],
            'key_error': [
                {
                    'pattern': r"'(\w+)'",
                    'fix': "Use dict.get('{0}', default_value) for safe access",
                    'example': "value = my_dict.get('key', 0)  # Returns 0 if key doesn't exist"
                }
            ],
            'zero_division_error': [
                {
                    'pattern': r'division by zero',
                    'fix': "Check if denominator is zero before division",
                    'example': "if y != 0: result = x / y else: result = float('inf')"
                }
            ],
            'import_error': [
                {
                    'pattern': r"No module named '(\w+)'",
                    'fix': "Install {0} using: pip install {0}",
                    'example': "pip install requests"
                }
            ],
            'memory_error': [
                {
                    'pattern': r'out of memory',
                    'fix': "Process data in chunks or use generators",
                    'example': "for chunk in pd.read_csv('large.csv', chunksize=10000): process(chunk)"
                }
            ],
            'timeout_error': [
                {
                    'pattern': r'timed out',
                    'fix': "Optimize algorithm or increase timeout limit",
                    'example': "Use caching: from functools import lru_cache"
                }
            ]
        }

    def suggest_fix(self, error: Error) -> List[Dict[str, Any]]:
        """Suggest fixes for an error"""
        suggestions = []
        error_msg = error.error_message
        error_type = error.error_type
        
        # Get templates for this error type
        templates = self.fix_templates.get(error_type, [])
        
        for template in templates:
            import re
            match = re.search(template['pattern'], error_msg, re.IGNORECASE)
            
            if match:
                # Generate fix with captured groups
                fix = template['fix'].format(*match.groups())
                suggestions.append({
                    'fix': fix,
                    'example': template.get('example', ''),
                    'confidence': 'high' if match.groups() else 'medium',
                    'type': 'specific'
                })
        
        # Add general suggestions if no specific matches
        if not suggestions:
            general_fixes = self._get_general_fixes(error_type, error_msg)
            suggestions.extend(general_fixes)
        
        # Add learned fixes from history
        if self.learning_enabled:
            learned = self._get_learned_fixes(error)
            suggestions.extend(learned)
        
        return suggestions

    def _get_general_fixes(
        self,
        error_type: str,
        error_msg: str
    ) -> List[Dict[str, Any]]:
        """Get general fixes for error type"""
        fixes = []
        
        # Error type specific general advice
        advice = {
            'syntax_error': {
                'fix': "Use a linter to catch syntax errors",
                'example': "Run: pylint your_file.py"
            },
            'name_error': {
                'fix': "Check variable scope and imports",
                'example': "from module import function"
            },
            'type_error': {
                'fix': "Add type checking with isinstance()",
                'example': "if isinstance(x, int): process(x)"
            },
            'value_error': {
                'fix': "Validate input before processing",
                'example': "try: value = int(input_string) except ValueError: handle_error()"
            },
            'attribute_error': {
                'fix': "Check object type with dir() or hasattr()",
                'example': "if hasattr(obj, 'method'): obj.method()"
            },
            'index_error': {
                'fix': "Use safe indexing with bounds checking",
                'example': "if 0 <= index < len(my_list): value = my_list[index]"
            },
            'key_error': {
                'fix': "Use defaultdict for missing keys",
                'example': "from collections import defaultdict; d = defaultdict(int)"
            },
            'zero_division_error': {
                'fix': "Add epsilon to denominator",
                'example': "result = x / (y + 1e-10)  # Avoid division by zero"
            },
            'import_error': {
                'fix': "Check requirements.txt for missing dependencies",
                'example': "pip install -r requirements.txt"
            },
            'memory_error': {
                'fix': "Use memory profiling to identify leaks",
                'example': "pip install memory_profiler"
            },
            'timeout_error': {
                'fix': "Implement caching for repeated computations",
                'example': "@lru_cache(maxsize=128) def expensive_function():"
            }
        }
        
        if error_type in advice:
            fixes.append({
                'fix': advice[error_type]['fix'],
                'example': advice[error_type]['example'],
                'confidence': 'medium',
                'type': 'general'
            })
        
        return fixes

    def _get_learned_fixes(self, error: Error) -> List[Dict[str, Any]]:
        """Get fixes learned from successful resolutions"""
        fixes = []
        
        # Look for similar errors that were successfully fixed
        for fix_record in self.successful_fixes[-20:]:  # Check last 20 fixes
            if fix_record.get('error_type') == error.error_type:
                similarity = self._calculate_similarity(
                    error.error_message,
                    fix_record.get('error_message', '')
                )
                
                if similarity > 0.7:  # High similarity
                    fixes.append({
                        'fix': fix_record.get('applied_fix'),
                        'example': fix_record.get('result', ''),
                        'confidence': 'medium' if similarity > 0.8 else 'low',
                        'type': 'learned',
                        'similarity': similarity
                    })
        
        return fixes

    def _calculate_similarity(self, msg1: str, msg2: str) -> float:
        """Calculate similarity between two error messages"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, msg1.lower(), msg2.lower()).ratio()

    def record_successful_fix(
        self,
        error: Error,
        applied_fix: str,
        result: str
    ) -> None:
        """Record a successful fix for learning"""
        self.successful_fixes.append({
            'error_type': error.error_type,
            'error_message': error.error_message,
            'applied_fix': applied_fix,
            'result': result,
            'timestamp': datetime.now()
        })
        
        # Keep only last 100 fixes
        if len(self.successful_fixes) > 100:
            self.successful_fixes = self.successful_fixes[-100:]

    def suggest_code_improvements(self, code: str) -> List[Dict[str, Any]]:
        """Suggest improvements for code quality"""
        suggestions = []
        
        try:
            tree = ast.parse(code)
            
            # Check for common code smells
            for node in ast.walk(tree):
                # Long functions
                if isinstance(node, ast.FunctionDef):
                    line_count = len(code.split('\n')[node.lineno-1:node.end_lineno])
                    if line_count > 20:
                        suggestions.append({
                            'type': 'code_smell',
                            'suggestion': f"Function '{node.name}' is too long ({line_count} lines)",
                            'fix': "Consider breaking it into smaller functions",
                            'line': node.lineno
                        })
                
                # Deep nesting
                if isinstance(node, ast.If):
                    nesting = self._get_nesting_level(node)
                    if nesting > 3:
                        suggestions.append({
                            'type': 'code_smell',
                            'suggestion': f"Deep nesting detected at line {node.lineno}",
                            'fix': "Consider early returns or guard clauses",
                            'line': node.lineno
                        })
                
                # Repeated code
                # This would require more sophisticated analysis
            
            # Check for missing docstrings
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    if not ast.get_docstring(node):
                        suggestions.append({
                            'type': 'documentation',
                            'suggestion': f"Missing docstring for {node.name}",
                            'fix': "Add docstring describing purpose and parameters",
                            'line': node.lineno
                        })
            
        except Exception as e:
            logger.debug(f"Code analysis failed: {e}")
        
        return suggestions

    def _get_nesting_level(self, node: ast.AST, level: int = 0) -> int:
        """Get nesting level of AST node"""
        max_level = level
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                max_level = max(max_level, self._get_nesting_level(child, level + 1))
        return max_level