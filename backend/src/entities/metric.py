
from datetime import datetime
from typing import Dict, Any, Optional
import secrets
import json


class Metric:
    def __init__(
        self,
        result_id: str,
        metric_name: str,
        metric_value: float,
        metric_id: Optional[str] = None
    ):
        self.metric_id = metric_id or self._generate_id()
        self.result_id = result_id
        self.metric_name = metric_name
        self.metric_value = metric_value
        self.details: Dict[str, Any] = {}
        self.calculated_at = datetime.now()
        self.normalized_value: Optional[float] = None
        self.threshold: Optional[float] = None
        self.weight: float = 1.0
        self.metadata: Dict[str, Any] = {}

    def _generate_id(self) -> str:
        """Generate a unique metric ID"""
        return f"met_{secrets.token_hex(8)}"

    def set_details(self, details: Dict[str, Any]) -> None:
        """Set detailed calculation data"""
        self.details = details

    def normalize(
        self,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        target_range: tuple = (0, 1)
    ) -> float:
        """Normalize metric value to target range"""
        if min_value is not None and max_value is not None:
            # Min-max normalization
            if max_value == min_value:
                self.normalized_value = target_range[0]
            else:
                self.normalized_value = (
                    (self.metric_value - min_value) / (max_value - min_value) *
                    (target_range[1] - target_range[0]) + target_range[0]
                )
        elif hasattr(self, 'range') and self.range:
            # Use predefined range
            min_val, max_val = self.range
            if max_val == min_val:
                self.normalized_value = target_range[0]
            else:
                self.normalized_value = (
                    (self.metric_value - min_val) / (max_val - min_val) *
                    (target_range[1] - target_range[0]) + target_range[0]
                )
        else:
            self.normalized_value = self.metric_value
        
        return self.normalized_value

    def set_threshold(self, threshold: float) -> None:
        """Set threshold for this metric"""
        self.threshold = threshold

    def is_passing(self) -> Optional[bool]:
        """Check if metric passes threshold"""
        if self.threshold is None:
            return None
        
        higher_is_better = self.metadata.get('higher_is_better', True)
        if higher_is_better:
            return self.metric_value >= self.threshold
        else:
            return self.metric_value <= self.threshold

    def compare(self, other: 'Metric') -> float:
        """Compare with another metric"""
        if self.metric_name != other.metric_name:
            raise ValueError("Cannot compare different metric types")
        
        return self.metric_value - other.metric_value

    def to_dict(self) -> Dict[str, Any]:
        """Convert metric to dictionary"""
        return {
            'metric_id': self.metric_id,
            'result_id': self.result_id,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'normalized_value': self.normalized_value,
            'details': self.details,
            'threshold': self.threshold,
            'weight': self.weight,
            'calculated_at': self.calculated_at.isoformat(),
            'metadata': self.metadata,
            'is_passing': self.is_passing()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Metric':
        """Create metric from dictionary"""
        metric = cls(
            result_id=data['result_id'],
            metric_name=data['metric_name'],
            metric_value=data['metric_value'],
            metric_id=data.get('metric_id')
        )
        metric.details = data.get('details', {})
        metric.normalized_value = data.get('normalized_value')
        metric.threshold = data.get('threshold')
        metric.weight = data.get('weight', 1.0)
        metric.calculated_at = datetime.fromisoformat(data['calculated_at']) if 'calculated_at' in data else datetime.now()
        metric.metadata = data.get('metadata', {})
        return metric

    @classmethod
    def create_pass_rate(cls, result_id: str, passed: int, total: int) -> 'Metric':
        """Create a pass rate metric"""
        value = passed / total if total > 0 else 0
        metric = cls(
            result_id=result_id,
            metric_name='pass_rate',
            metric_value=value
        )
        metric.metadata = {
            'higher_is_better': True,
            'range': (0, 1),
            'description': 'Percentage of passing tests'
        }
        metric.set_details({
            'passed': passed,
            'total': total
        })
        return metric

    @classmethod
    def create_execution_time(cls, result_id: str, time_ms: float) -> 'Metric':
        """Create an execution time metric"""
        metric = cls(
            result_id=result_id,
            metric_name='execution_time',
            metric_value=time_ms
        )
        metric.metadata = {
            'higher_is_better': False,
            'range': (0, float('inf')),
            'description': 'Execution time in milliseconds',
            'unit': 'ms'
        }
        return metric

    @classmethod
    def create_codebleu(cls, result_id: str, score: float, components: Dict[str, float]) -> 'Metric':
        """Create a CodeBLEU metric"""
        metric = cls(
            result_id=result_id,
            metric_name='codebleu',
            metric_value=score
        )
        metric.metadata = {
            'higher_is_better': True,
            'range': (0, 1),
            'description': 'CodeBLEU score for semantic similarity'
        }
        metric.set_details({
            'components': components,
            'bleu': components.get('bleu', 0),
            'syntax_match': components.get('syntax_match', 0),
            'dataflow_match': components.get('dataflow_match', 0)
        })
        return metric