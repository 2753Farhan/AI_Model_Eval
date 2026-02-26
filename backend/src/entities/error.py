
from datetime import datetime
from typing import List, Dict, Any, Optional
import secrets
import re


class Error:
    def __init__(
        self,
        result_id: str,
        error_type: str,
        error_message: str,
        error_id: Optional[str] = None
    ):
        self.error_id = error_id or self._generate_id()
        self.result_id = result_id
        self.error_type = error_type  # syntax, semantic, runtime, logical, timeout
        self.error_message = error_message
        self.error_location: Optional[Dict[str, Any]] = None
        self.severity: str = "error"  # error, warning, info
        self.stack_trace: Optional[str] = None
        self.suggested_fix: Optional[str] = None
        self.pattern_id: Optional[str] = None
        self.metadata: Dict[str, Any] = {}
        self.recorded_at = datetime.now()
        self.frequency: int = 1

    def _generate_id(self) -> str:
        """Generate a unique error ID"""
        return f"err_{secrets.token_hex(8)}"

    def set_location(
        self,
        line: Optional[int] = None,
        column: Optional[int] = None,
        file: Optional[str] = None,
        function: Optional[str] = None
    ) -> None:
        """Set error location"""
        self.error_location = {
            'line': line,
            'column': column,
            'file': file,
            'function': function
        }

    def set_stack_trace(self, stack_trace: str) -> None:
        """Set stack trace"""
        self.stack_trace = stack_trace

    def suggest_fix(self, fix: str) -> None:
        """Suggest a fix for this error"""
        self.suggested_fix = fix

    def set_pattern(self, pattern_id: str) -> None:
        """Set the pattern ID for this error"""
        self.pattern_id = pattern_id

    def increment_frequency(self) -> None:
        """Increment error frequency"""
        self.frequency += 1

    def classify_severity(self) -> str:
        """Classify error severity based on type and message"""
        if self.error_type in ['timeout', 'memory_error']:
            self.severity = 'critical'
        elif self.error_type in ['runtime', 'logical']:
            self.severity = 'error'
        elif self.error_type in ['syntax', 'semantic']:
            self.severity = 'warning'
        else:
            self.severity = 'info'
        
        return self.severity

    def extract_pattern_signature(self) -> str:
        """Extract a pattern signature from the error message"""
        # Remove variable parts (numbers, specific names)
        pattern = self.error_message
        
        # Replace numbers with placeholders
        pattern = re.sub(r'\d+', '{num}', pattern)
        
        # Replace quoted strings with placeholders
        pattern = re.sub(r'"[^"]*"', '{str}', pattern)
        pattern = re.sub(r"'[^']*'", '{str}', pattern)
        
        # Replace variable names (common patterns)
        pattern = re.sub(r'\b[a-z][a-z0-9_]*\b', '{var}', pattern)
        
        return pattern

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary"""
        return {
            'error_id': self.error_id,
            'result_id': self.result_id,
            'error_type': self.error_type,
            'error_message': self.error_message,
            'error_location': self.error_location,
            'severity': self.severity,
            'stack_trace': self.stack_trace,
            'suggested_fix': self.suggested_fix,
            'pattern_id': self.pattern_id,
            'metadata': self.metadata,
            'recorded_at': self.recorded_at.isoformat(),
            'frequency': self.frequency,
            'pattern_signature': self.extract_pattern_signature()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Error':
        """Create error from dictionary"""
        error = cls(
            result_id=data['result_id'],
            error_type=data['error_type'],
            error_message=data['error_message'],
            error_id=data.get('error_id')
        )
        error.error_location = data.get('error_location')
        error.severity = data.get('severity', 'error')
        error.stack_trace = data.get('stack_trace')
        error.suggested_fix = data.get('suggested_fix')
        error.pattern_id = data.get('pattern_id')
        error.metadata = data.get('metadata', {})
        error.recorded_at = datetime.fromisoformat(data['recorded_at']) if 'recorded_at' in data else datetime.now()
        error.frequency = data.get('frequency', 1)
        return error

    @classmethod
    def from_exception(cls, result_id: str, exception: Exception) -> 'Error':
        """Create error from exception"""
        error_type = type(exception).__name__
        error_msg = str(exception)
        
        # Categorize error type
        if 'timeout' in error_msg.lower():
            category = 'timeout'
        elif 'memory' in error_msg.lower():
            category = 'memory_error'
        elif 'syntax' in error_msg.lower():
            category = 'syntax'
        elif 'name' in error_msg.lower() and 'is not defined' in error_msg:
            category = 'semantic'
        else:
            category = 'runtime'
        
        error = cls(
            result_id=result_id,
            error_type=category,
            error_message=error_msg
        )
        error.classify_severity()
        return error