
from datetime import datetime
from typing import List, Dict, Any, Optional
import secrets
import numpy as np


class Benchmark:
    def __init__(
        self,
        name: str,
        description: str,
        benchmark_id: Optional[str] = None
    ):
        self.benchmark_id = benchmark_id or self._generate_id()
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.models: List[Dict[str, Any]] = []
        self.metrics: List[str] = []
        self.results: Dict[str, Dict[str, float]] = {}  # model_id -> metric -> score
        self.rankings: Dict[str, int] = {}
        self.scores: Dict[str, float] = {}
        self.metadata: Dict[str, Any] = {}

    def _generate_id(self) -> str:
        """Generate a unique benchmark ID"""
        return f"ben_{secrets.token_hex(8)}"

    def add_model(self, model_id: str, model_name: str, metadata: Optional[Dict] = None) -> None:
        """Add a model to the benchmark"""
        self.models.append({
            'model_id': model_id,
            'model_name': model_name,
            'metadata': metadata or {}
        })

    def add_metric(self, metric_name: str, weight: float = 1.0) -> None:
        """Add a metric to the benchmark"""
        self.metrics.append(metric_name)

    def add_result(self, model_id: str, metric_name: str, score: float) -> None:
        """Add a result for a model and metric"""
        if model_id not in self.results:
            self.results[model_id] = {}
        self.results[model_id][metric_name] = score
        self.updated_at = datetime.now()

    def calculate_scores(self, weights: Optional[Dict[str, float]] = None) -> Dict[str, float]:
        """Calculate aggregate scores for all models"""
        if not weights:
            # Default equal weights
            weights = {metric: 1.0 for metric in self.metrics}
        
        # Normalize weights
        total_weight = sum(weights.values())
        if total_weight > 0:
            weights = {k: v / total_weight for k, v in weights.items()}
        
        scores = {}
        for model_id, model_results in self.results.items():
            score = 0.0
            for metric, weight in weights.items():
                if metric in model_results:
                    score += model_results[metric] * weight
            scores[model_id] = score
        
        self.scores = scores
        return scores

    def calculate_rankings(self) -> Dict[str, int]:
        """Calculate rankings based on aggregate scores"""
        if not self.scores:
            self.calculate_scores()
        
        sorted_models = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        rankings = {}
        for rank, (model_id, _) in enumerate(sorted_models, 1):
            rankings[model_id] = rank
        
        self.rankings = rankings
        return rankings

    def compare_models(
        self,
        model_id1: str,
        model_id2: str,
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Compare two models"""
        if model_id1 not in self.results or model_id2 not in self.results:
            raise ValueError("One or both models not found in benchmark")
        
        metrics_to_compare = metrics or self.metrics
        
        comparison = {
            'model1': model_id1,
            'model2': model_id2,
            'metrics': {},
            'model1_wins': 0,
            'model2_wins': 0,
            'ties': 0
        }
        
        for metric in metrics_to_compare:
            score1 = self.results[model_id1].get(metric, 0)
            score2 = self.results[model_id2].get(metric, 0)
            
            comparison['metrics'][metric] = {
                'model1': score1,
                'model2': score2,
                'difference': score1 - score2
            }
            
            if score1 > score2:
                comparison['model1_wins'] += 1
            elif score2 > score1:
                comparison['model2_wins'] += 1
            else:
                comparison['ties'] += 1
        
        return comparison

    def get_top_models(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get top N models"""
        if not self.rankings:
            self.calculate_rankings()
        
        top_model_ids = sorted(self.rankings.items(), key=lambda x: x[1])[:n]
        
        top_models = []
        for model_id, rank in top_model_ids:
            model_info = next((m for m in self.models if m['model_id'] == model_id), {})
            top_models.append({
                'rank': rank,
                'model_id': model_id,
                'model_name': model_info.get('model_name', model_id),
                'score': self.scores.get(model_id, 0),
                'metrics': self.results.get(model_id, {})
            })
        
        return top_models

    def to_dict(self) -> Dict[str, Any]:
        """Convert benchmark to dictionary"""
        return {
            'benchmark_id': self.benchmark_id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'models': self.models,
            'metrics': self.metrics,
            'results': self.results,
            'rankings': self.rankings or self.calculate_rankings(),
            'scores': self.scores or self.calculate_scores(),
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Benchmark':
        """Create benchmark from dictionary"""
        benchmark = cls(
            name=data['name'],
            description=data['description'],
            benchmark_id=data.get('benchmark_id')
        )
        benchmark.created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        benchmark.updated_at = datetime.fromisoformat(data['updated_at']) if 'updated_at' in data else datetime.now()
        benchmark.models = data.get('models', [])
        benchmark.metrics = data.get('metrics', [])
        benchmark.results = data.get('results', {})
        benchmark.rankings = data.get('rankings', {})
        benchmark.scores = data.get('scores', {})
        benchmark.metadata = data.get('metadata', {})
        return benchmark

    @classmethod
    def create_humaneval_benchmark(cls) -> 'Benchmark':
        """Create a benchmark for HumanEval"""
        benchmark = cls(
            name="HumanEval Benchmark",
            description="Standard benchmark for code generation models on HumanEval dataset"
        )
        benchmark.add_metric('pass@1', weight=0.4)
        benchmark.add_metric('pass@5', weight=0.3)
        benchmark.add_metric('codebleu', weight=0.2)
        benchmark.add_metric('execution_time', weight=0.1)
        return benchmark