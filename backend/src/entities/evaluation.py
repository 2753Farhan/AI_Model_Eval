
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import secrets
from enum import Enum


class EvaluationStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Evaluation:
    def __init__(
        self,
        user_id: str,
        config: Dict[str, Any],
        evaluation_id: Optional[str] = None
    ):
        self.evaluation_id = evaluation_id or self._generate_id()
        self.user_id = user_id
        self.model_ids: List[str] = []
        self.dataset_id: Optional[str] = None
        self.status = EvaluationStatus.PENDING
        self.config = config
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.progress: float = 0.0
        self.current_stage: str = "initializing"
        self.results_ids: List[str] = []
        self.report_ids: List[str] = []
        self.error_message: Optional[str] = None
        self.metadata: Dict[str, Any] = {}
        self.notes: str = ""

    def _generate_id(self) -> str:
        """Generate a unique evaluation ID"""
        return f"eval_{secrets.token_hex(8)}"

    def start(self) -> bool:
        """Start the evaluation"""
        if self.status not in [EvaluationStatus.PENDING, EvaluationStatus.PAUSED]:
            return False
        self.status = EvaluationStatus.RUNNING
        self.started_at = datetime.now()
        self.current_stage = "starting"
        return True

    def pause(self) -> bool:
        """Pause the evaluation"""
        if self.status != EvaluationStatus.RUNNING:
            return False
        self.status = EvaluationStatus.PAUSED
        self.current_stage = "paused"
        return True

    def resume(self) -> bool:
        """Resume the evaluation"""
        if self.status != EvaluationStatus.PAUSED:
            return False
        self.status = EvaluationStatus.RUNNING
        self.current_stage = "resumed"
        return True

    def cancel(self) -> bool:
        """Cancel the evaluation"""
        if self.status in [EvaluationStatus.COMPLETED, EvaluationStatus.FAILED]:
            return False
        self.status = EvaluationStatus.CANCELLED
        self.completed_at = datetime.now()
        self.current_stage = "cancelled"
        return True

    def complete(self) -> None:
        """Mark evaluation as completed"""
        self.status = EvaluationStatus.COMPLETED
        self.completed_at = datetime.now()
        self.progress = 100.0
        self.current_stage = "completed"

    def fail(self, error_message: str) -> None:
        """Mark evaluation as failed"""
        self.status = EvaluationStatus.FAILED
        self.completed_at = datetime.now()
        self.error_message = error_message
        self.current_stage = "failed"

    def update_progress(self, progress: float, stage: str) -> None:
        """Update evaluation progress"""
        self.progress = min(max(progress, 0.0), 100.0)
        self.current_stage = stage

    def add_model(self, model_id: str) -> None:
        """Add a model to the evaluation"""
        if model_id not in self.model_ids:
            self.model_ids.append(model_id)

    def set_dataset(self, dataset_id: str) -> None:
        """Set the dataset for evaluation"""
        self.dataset_id = dataset_id

    def add_result(self, result_id: str) -> None:
        """Add a result ID to the evaluation"""
        if result_id not in self.results_ids:
            self.results_ids.append(result_id)

    def add_report(self, report_id: str) -> None:
        """Add a report ID to the evaluation"""
        if report_id not in self.report_ids:
            self.report_ids.append(report_id)

    def get_duration(self) -> Optional[float]:
        """Get evaluation duration in seconds"""
        if not self.started_at:
            return None
        end_time = self.completed_at or datetime.now()
        return (end_time - self.started_at).total_seconds()

    def to_dict(self) -> Dict[str, Any]:
        """Convert evaluation to dictionary"""
        return {
            'evaluation_id': self.evaluation_id,
            'user_id': self.user_id,
            'model_ids': self.model_ids,
            'dataset_id': self.dataset_id,
            'status': self.status.value,
            'config': self.config,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'progress': self.progress,
            'current_stage': self.current_stage,
            'results_ids': self.results_ids,
            'report_ids': self.report_ids,
            'error_message': self.error_message,
            'metadata': self.metadata,
            'notes': self.notes,
            'duration': self.get_duration()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Evaluation':
        """Create evaluation from dictionary"""
        eval_obj = cls(
            user_id=data['user_id'],
            config=data['config'],
            evaluation_id=data.get('evaluation_id')
        )
        eval_obj.model_ids = data.get('model_ids', [])
        eval_obj.dataset_id = data.get('dataset_id')
        eval_obj.status = EvaluationStatus(data.get('status', 'pending'))
        eval_obj.created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        eval_obj.started_at = datetime.fromisoformat(data['started_at']) if data.get('started_at') else None
        eval_obj.completed_at = datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None
        eval_obj.progress = data.get('progress', 0.0)
        eval_obj.current_stage = data.get('current_stage', 'initializing')
        eval_obj.results_ids = data.get('results_ids', [])
        eval_obj.report_ids = data.get('report_ids', [])
        eval_obj.error_message = data.get('error_message')
        eval_obj.metadata = data.get('metadata', {})
        eval_obj.notes = data.get('notes', '')
        return eval_obj