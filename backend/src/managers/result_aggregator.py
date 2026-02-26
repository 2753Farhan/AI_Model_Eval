
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import pandas as pd
from collections import defaultdict
from datetime import datetime, timedelta

from ..entities import EvaluationResult, Metric, Error, Benchmark


class ResultAggregator:
    def __init__(self):
        self.results: Dict[str, List[EvaluationResult]] = defaultdict(list)
        self.benchmarks: Dict[str, Benchmark] = {}

    def add_results(self, evaluation_id: str, results: List[EvaluationResult]) -> None:
        """Add results for aggregation"""
        self.results[evaluation_id].extend(results)

    def aggregate_by_model(
        self,
        evaluation_id: str
    ) -> Dict[str, Dict[str, Any]]:
        """Aggregate results by model"""
        results = self.results.get(evaluation_id, [])
        if not results:
            return {}
        
        model_results = defaultdict(list)
        for result in results:
            model_results[result.model_id].append(result)
        
        aggregation = {}
        for model_id, model_results_list in model_results.items():
            aggregation[model_id] = self._aggregate_model_results(model_results_list)
        
        return aggregation

    def _aggregate_model_results(
        self,
        results: List[EvaluationResult]
    ) -> Dict[str, Any]:
        """Aggregate results for a single model"""
        if not results:
            return {}
        
        # Calculate pass rate
        passed = sum(1 for r in results if r.passed)
        total = len(results)
        
        # Collect metrics
        metrics = defaultdict(list)
        for result in results:
            for name, value in result.metrics.items():
                metrics[name].append(value)
        
        # Calculate statistics
        stats = {
            'total_evaluations': total,
            'passed': passed,
            'failed': total - passed,
            'pass_rate': passed / total if total > 0 else 0,
            'metrics': {}
        }
        
        for name, values in metrics.items():
            if values:
                stats['metrics'][name] = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'min': np.min(values),
                    'max': np.max(values),
                    'median': np.median(values),
                    'count': len(values)
                }
        
        # Error analysis
        all_errors = []
        for result in results:
            all_errors.extend(result.errors)
        
        stats['errors'] = self._aggregate_errors(all_errors)
        
        return stats

    def _aggregate_errors(self, errors: List[Dict]) -> Dict[str, Any]:
        """Aggregate error statistics"""
        if not errors:
            return {'total': 0}
        
        error_types = defaultdict(int)
        severities = defaultdict(int)
        
        for error in errors:
            error_types[error.get('error_type', 'unknown')] += 1
            severities[error.get('severity', 'error')] += 1
        
        return {
            'total': len(errors),
            'by_type': dict(error_types),
            'by_severity': dict(severities),
            'unique_patterns': len(set(e.get('pattern_id') for e in errors if e.get('pattern_id')))
        }

    def compare_models(
        self,
        evaluation_id: str,
        model_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Compare multiple models"""
        aggregation = self.aggregate_by_model(evaluation_id)
        
        if model_ids:
            aggregation = {k: v for k, v in aggregation.items() if k in model_ids}
        
        if not aggregation:
            return {}
        
        # Create comparison
        comparison = {
            'models': list(aggregation.keys()),
            'pass_rates': {},
            'metrics_comparison': {},
            'ranking': []
        }
        
        # Collect pass rates
        for model_id, stats in aggregation.items():
            comparison['pass_rates'][model_id] = stats['pass_rate']
        
        # Compare each metric
        all_metrics = set()
        for stats in aggregation.values():
            all_metrics.update(stats.get('metrics', {}).keys())
        
        for metric in all_metrics:
            comparison['metrics_comparison'][metric] = {}
            for model_id, stats in aggregation.items():
                if metric in stats.get('metrics', {}):
                    comparison['metrics_comparison'][metric][model_id] = \
                        stats['metrics'][metric]['mean']
        
        # Rank models by pass rate
        comparison['ranking'] = sorted(
            comparison['pass_rates'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return comparison

    def create_benchmark(
        self,
        name: str,
        description: str,
        evaluation_ids: List[str],
        metric_weights: Optional[Dict[str, float]] = None
    ) -> Benchmark:
        """Create a benchmark from multiple evaluations"""
        benchmark = Benchmark(name=name, description=description)
        
        # Collect all results
        all_results = []
        for eval_id in evaluation_ids:
            all_results.extend(self.results.get(eval_id, []))
        
        if not all_results:
            return benchmark
        
        # Group by model
        model_results = defaultdict(list)
        for result in all_results:
            model_results[result.model_id].append(result)
        
        # Add models to benchmark
        for model_id, results in model_results.items():
            # Get model name from first result's metadata
            model_name = results[0].metadata.get('model_name', model_id)
            benchmark.add_model(model_id, model_name)
        
        # Add metrics
        if metric_weights:
            for metric, weight in metric_weights.items():
                benchmark.add_metric(metric, weight)
        else:
            # Default metrics
            benchmark.add_metric('pass_rate', weight=0.4)
            benchmark.add_metric('execution_time', weight=0.2)
            benchmark.add_metric('code_quality', weight=0.2)
            benchmark.add_metric('error_count', weight=0.2)
        
        # Add results
        for model_id, results in model_results.items():
            # Calculate aggregate metrics
            stats = self._aggregate_model_results(results)
            
            for metric in benchmark.metrics:
                if metric == 'pass_rate':
                    benchmark.add_result(model_id, metric, stats['pass_rate'])
                elif metric == 'execution_time':
                    # Average execution time (normalized)
                    times = [r.execution_time_ms for r in results if r.execution_time_ms]
                    avg_time = np.mean(times) if times else float('inf')
                    benchmark.add_result(model_id, metric, avg_time)
                elif metric == 'error_count':
                    benchmark.add_result(model_id, metric, stats['errors']['total'])
                elif metric == 'code_quality':
                    # Composite quality score
                    quality_scores = []
                    for result in results:
                        if 'maintainability_index' in result.metrics:
                            quality_scores.append(result.metrics['maintainability_index'])
                    avg_quality = np.mean(quality_scores) if quality_scores else 0
                    benchmark.add_result(model_id, metric, avg_quality)
        
        # Calculate rankings
        benchmark.calculate_scores()
        benchmark.calculate_rankings()
        
        # Store benchmark
        self.benchmarks[benchmark.benchmark_id] = benchmark
        
        return benchmark

    def get_performance_trends(
        self,
        evaluation_ids: List[str],
        model_id: Optional[str] = None,
        time_window: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        trends = {
            'pass_rate': [],
            'execution_time': [],
            'error_rate': [],
            'timestamps': []
        }
        
        for eval_id in evaluation_ids:
            results = self.results.get(eval_id, [])
            
            if model_id:
                results = [r for r in results if r.model_id == model_id]
            
            if not results:
                continue
            
            # Get evaluation time from first result
            eval_time = min(r.created_at for r in results)
            
            if time_window and datetime.now() - eval_time > time_window:
                continue
            
            # Calculate metrics for this evaluation
            passed = sum(1 for r in results if r.passed)
            total = len(results)
            
            trends['timestamps'].append(eval_time)
            trends['pass_rate'].append(passed / total if total > 0 else 0)
            
            # Average execution time
            times = [r.execution_time_ms for r in results if r.execution_time_ms]
            trends['execution_time'].append(np.mean(times) if times else 0)
            
            # Error rate
            errors = sum(len(r.errors) for r in results)
            trends['error_rate'].append(errors / total if total > 0 else 0)
        
        return trends

    def export_to_dataframe(self, evaluation_id: str) -> pd.DataFrame:
        """Export results to pandas DataFrame"""
        results = self.results.get(evaluation_id, [])
        
        data = []
        for result in results:
            row = {
                'result_id': result.result_id,
                'model_id': result.model_id,
                'problem_id': result.problem_id,
                'sample_id': result.sample_id,
                'passed': result.passed,
                'execution_time_ms': result.execution_time_ms,
                'memory_usage_kb': result.memory_usage_kb,
                'created_at': result.created_at,
                'error_count': len(result.errors)
            }
            
            # Add metrics
            for name, value in result.metrics.items():
                row[f'metric_{name}'] = value
            
            data.append(row)
        
        return pd.DataFrame(data)