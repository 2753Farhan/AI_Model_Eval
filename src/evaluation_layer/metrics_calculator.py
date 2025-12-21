import pandas as pd
import numpy as np
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class MetricsCalculator:
    def __init__(self):
        pass
    
    def calculate_pass_at_k(self, results_df: pd.DataFrame, k_values: List[int] = [1, 5, 10]) -> Dict:
        """Calculate pass@k metrics from the paper"""
        metrics = {}
        
        for k in k_values:
            pass_at_k = self._estimate_pass_at_k(results_df, k)
            metrics[f'pass@{k}'] = pass_at_k
        
        return metrics
    
    def _estimate_pass_at_k(self, results_df: pd.DataFrame, k: int) -> float:
        """Estimate pass@k using unbiased estimator"""
        # Group by problem and model
        grouped = results_df.groupby(['task_id', 'model'])
        
        pass_rates = []
        
        for (task_id, model), group in grouped:
            # Get all samples for this problem-model combination
            samples = group['passed'].tolist()
            n = len(samples)
            c = sum(samples)
            
            if n < k:
                continue  # Not enough samples
            
            # Calculate pass@k using unbiased estimator
            if n - c < k:
                pass_rate = 1.0
            else:
                pass_rate = 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))
            
            pass_rates.append(pass_rate)
        
        return np.mean(pass_rates) if pass_rates else 0.0
    
    def calculate_aggregate_score(self, functional_scores: Dict, static_scores: pd.DataFrame) -> float:
        """Calculate aggregate performance score"""
        # Weight functional correctness higher
        functional_weight = 0.7
        static_weight = 0.3
        
        # Normalize functional scores (pass@1 as primary metric)
        functional_normalized = functional_scores.get('pass@1', 0)
        
        # Calculate static quality score (average of normalized metrics)
        if not static_scores.empty:
            maintainability_norm = static_scores['maintainability_index'].mean() / 100
            complexity_norm = 1 - (static_scores['cyclomatic_complexity'].mean() / 20)  # Normalize
            static_normalized = (maintainability_norm + complexity_norm) / 2
        else:
            static_normalized = 0
        
        aggregate_score = (functional_normalized * functional_weight + 
                          static_normalized * static_weight)
        
        return aggregate_score
    
    def generate_comparison_report(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """Generate comparative report across models"""
        report_data = []
        
        for model in results_df['model'].unique():
            model_results = results_df[results_df['model'] == model]
            
            # Calculate metrics
            total_tests = len(model_results)
            passed_tests = model_results['passed'].sum()
            pass_rate = passed_tests / total_tests if total_tests > 0 else 0
            
            # Calculate pass@k for this model
            model_pass_at_k = self.calculate_pass_at_k(model_results, [1, 5])
            
            report_data.append({
                'model': model,
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'pass_rate': pass_rate,
                'pass@1': model_pass_at_k.get('pass@1', 0),
                'pass@5': model_pass_at_k.get('pass@5', 0),
                'avg_execution_time': model_results.get('execution_time', pd.Series([0])).mean()
            })
        
        return pd.DataFrame(report_data)