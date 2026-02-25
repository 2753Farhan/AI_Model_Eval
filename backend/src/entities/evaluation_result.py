
from datetime import datetime
from typing import List, Dict, Any, Optional
import secrets
import json


class EvaluationResult:
    def __init__(
        self,
        evaluation_id: str,
        problem_id: str,
        model_id: str,
        sample_id: int,
        result_id: Optional[str] = None
    ):
        self.result_id = result_id or self._generate_id()
        self.evaluation_id = evaluation_id
        self.problem_id = problem_id
        self.model_id = model_id
        self.sample_id = sample_id
        self.generated_code: Optional[str] = None
        self.execution_output: Optional[str] = None
        self.passed: bool = False
        self.execution_time_ms: Optional[float] = None
        self.memory_usage_kb: Optional[float] = None
        self.test_results: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.metrics: Dict[str, float] = {}
        self.metadata: Dict[str, Any] = {}
        self.created_at = datetime.now()
        self.source: str = "generated"

    def _generate_id(self) -> str:
        """Generate a unique result ID"""
        return f"res_{secrets.token_hex(8)}"

    def set_generated_code(self, code: str) -> None:
        """Set the generated code"""
        self.generated_code = code

    def set_execution_result(
        self,
        passed: bool,
        output: str,
        execution_time_ms: float,
        memory_usage_kb: Optional[float] = None
    ) -> None:
        """Set execution results"""
        self.passed = passed
        self.execution_output = output
        self.execution_time_ms = execution_time_ms
        self.memory_usage_kb = memory_usage_kb

    def add_test_result(
        self,
        test_id: int,
        passed: bool,
        message: str,
        test_case: Optional[str] = None
    ) -> None:
        """Add a test result"""
        self.test_results.append({
            'test_id': test_id,
            'passed': passed,
            'message': message,
            'test_case': test_case
        })

    def add_error(
        self,
        error_type: str,
        error_message: str,
        severity: str = "error",
        location: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add an error"""
        self.errors.append({
            'error_id': len(self.errors),
            'error_type': error_type,
            'error_message': error_message,
            'severity': severity,
            'location': location,
            'timestamp': datetime.now().isoformat()
        })

    def add_metric(self, name: str, value: float) -> None:
        """Add a metric"""
        self.metrics[name] = value

    def calculate_metrics(self) -> Dict[str, float]:
        """Calculate aggregate metrics"""
        metrics = {}
        
        # Pass rate
        if self.test_results:
            passed = sum(1 for t in self.test_results if t.get('passed', False))
            metrics['pass_rate'] = passed / len(self.test_results)
        
        # Execution stats
        if self.execution_time_ms:
            metrics['execution_time'] = self.execution_time_ms
        
        if self.memory_usage_kb:
            metrics['memory_usage'] = self.memory_usage_kb
        
        # Error count
        metrics['error_count'] = len(self.errors)
        
        # Code quality metrics
        if self.generated_code:
            metrics['code_length'] = len(self.generated_code)
            metrics['line_count'] = len(self.generated_code.split('\n'))
        
        self.metrics.update(metrics)
        return metrics

    def is_passing(self) -> bool:
        """Check if all tests passed"""
        return self.passed and all(t.get('passed', False) for t in self.test_results)

    def get_error_analysis(self) -> Dict[str, Any]:
        """Get error analysis summary"""
        if not self.errors:
            return {'has_errors': False}
        
        error_types = {}
        for error in self.errors:
            error_type = error.get('error_type', 'unknown')
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            'has_errors': True,
            'total_errors': len(self.errors),
            'error_types': error_types,
            'first_error': self.errors[0] if self.errors else None
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            'result_id': self.result_id,
            'evaluation_id': self.evaluation_id,
            'problem_id': self.problem_id,
            'model_id': self.model_id,
            'sample_id': self.sample_id,
            'generated_code': self.generated_code,
            'execution_output': self.execution_output,
            'passed': self.passed,
            'execution_time_ms': self.execution_time_ms,
            'memory_usage_kb': self.memory_usage_kb,
            'test_results': self.test_results,
            'errors': self.errors,
            'metrics': self.metrics or self.calculate_metrics(),
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'source': self.source,
            'is_passing': self.is_passing()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EvaluationResult':
        """Create result from dictionary"""
        result = cls(
            evaluation_id=data['evaluation_id'],
            problem_id=data['problem_id'],
            model_id=data['model_id'],
            sample_id=data['sample_id'],
            result_id=data.get('result_id')
        )
        result.generated_code = data.get('generated_code')
        result.execution_output = data.get('execution_output')
        result.passed = data.get('passed', False)
        result.execution_time_ms = data.get('execution_time_ms')
        result.memory_usage_kb = data.get('memory_usage_kb')
        result.test_results = data.get('test_results', [])
        result.errors = data.get('errors', [])
        result.metrics = data.get('metrics', {})
        result.metadata = data.get('metadata', {})
        result.created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        result.source = data.get('source', 'generated')
        return result