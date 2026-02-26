from typing import List, Dict, Any, Optional, Union
import json
import csv
import os
from datetime import datetime
import logging
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Change from relative to absolute imports
from src.entities import Report, Evaluation, EvaluationResult, Benchmark
from .exporters import CSVExporter, JSONExporter, PDFExporter, HTMLExporter, MarkdownExporter

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates reports from evaluation results"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.generator_id = self._generate_id()
        self.output_dir = Path(config.get('output_dir', 'reports'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize exporters
        self.exporters = {
            'csv': CSVExporter(),
            'json': JSONExporter(),
            'pdf': PDFExporter(),
            'html': HTMLExporter(),
            'md': MarkdownExporter()
        }
        
        # Templates directory
        self.templates_dir = Path(__file__).parent / 'templates'
        
        logger.info(f"ReportGenerator initialized with output dir: {self.output_dir}")

    def _generate_id(self) -> str:
        """Generate a unique generator ID"""
        import secrets
        return f"gen_{secrets.token_hex(8)}"

    def generate_summary_report(
        self,
        evaluation: Evaluation,
        results: List[EvaluationResult],
        format: str = 'html'
    ) -> Report:
        """Generate a summary report"""
        report = Report(
            evaluation_id=evaluation.evaluation_id,
            report_type='summary',
            report_format=format
        )
        
        # Prepare summary data
        summary_data = self._prepare_summary_data(evaluation, results)
        report.add_summary(summary_data)
        
        # Generate charts
        charts = self._generate_summary_charts(results)
        for name, chart in charts.items():
            report.add_chart(name, chart)
        
        # Generate tables
        tables = self._generate_summary_tables(results)
        for table in tables:
            report.add_table(table)
        
        # Export to file
        if format in self.exporters:
            exporter = self.exporters[format]
            file_path = self.output_dir / report.get_filename()
            exporter.export(report, str(file_path))
            report.set_file_path(str(file_path))
        
        return report

    def generate_detailed_report(
        self,
        evaluation: Evaluation,
        results: List[EvaluationResult],
        format: str = 'html'
    ) -> Report:
        """Generate a detailed report"""
        report = Report(
            evaluation_id=evaluation.evaluation_id,
            report_type='detailed',
            report_format=format
        )
        
        # Prepare detailed data
        detailed_data = self._prepare_detailed_data(evaluation, results)
        report.add_detailed_data(detailed_data)
        
        # Generate detailed charts
        charts = self._generate_detailed_charts(results)
        for name, chart in charts.items():
            report.add_chart(name, chart)
        
        # Generate detailed tables
        tables = self._generate_detailed_tables(results)
        for table in tables:
            report.add_table(table)
        
        # Export to file
        if format in self.exporters:
            exporter = self.exporters[format]
            file_path = self.output_dir / report.get_filename()
            exporter.export(report, str(file_path))
            report.set_file_path(str(file_path))
        
        return report

    def generate_comparative_report(
        self,
        evaluations: List[Evaluation],
        results_dict: Dict[str, List[EvaluationResult]],
        benchmark: Optional[Benchmark] = None,
        format: str = 'html'
    ) -> Report:
        """Generate a comparative report across evaluations"""
        report = Report(
            evaluation_id='comparative',
            report_type='comparative',
            report_format=format
        )
        
        # Prepare comparative data
        comparative_data = self._prepare_comparative_data(evaluations, results_dict, benchmark)
        report.add_detailed_data(comparative_data)
        
        # Generate comparative charts
        charts = self._generate_comparative_charts(results_dict, benchmark)
        for name, chart in charts.items():
            report.add_chart(name, chart)
        
        # Generate comparative tables
        tables = self._generate_comparative_tables(results_dict, benchmark)
        for table in tables:
            report.add_table(table)
        
        # Export to file
        if format in self.exporters:
            exporter = self.exporters[format]
            file_path = self.output_dir / report.get_filename()
            exporter.export(report, str(file_path))
            report.set_file_path(str(file_path))
        
        return report

    def _prepare_summary_data(
        self,
        evaluation: Evaluation,
        results: List[EvaluationResult]
    ) -> Dict[str, Any]:
        """Prepare summary data"""
        total_results = len(results)
        passed_results = sum(1 for r in results if r.passed)
        
        # Aggregate metrics
        all_metrics = {}
        for result in results:
            for name, value in result.metrics.items():
                if name not in all_metrics:
                    all_metrics[name] = []
                all_metrics[name].append(value)
        
        avg_metrics = {}
        for name, values in all_metrics.items():
            avg_metrics[name] = sum(values) / len(values) if values else 0
        
        return {
            'evaluation_id': evaluation.evaluation_id,
            'created_at': evaluation.created_at.isoformat(),
            'duration': evaluation.get_duration(),
            'models': evaluation.model_ids,
            'total_results': total_results,
            'passed_results': passed_results,
            'pass_rate': passed_results / total_results if total_results > 0 else 0,
            'average_metrics': avg_metrics,
            'status': evaluation.status.value
        }

    def _prepare_detailed_data(
        self,
        evaluation: Evaluation,
        results: List[EvaluationResult]
    ) -> Dict[str, Any]:
        """Prepare detailed data"""
        summary = self._prepare_summary_data(evaluation, results)
        
        # Group by model
        model_results = {}
        for result in results:
            if result.model_id not in model_results:
                model_results[result.model_id] = []
            model_results[result.model_id].append(result)
        
        # Per-model statistics
        model_stats = {}
        for model_id, model_results_list in model_results.items():
            model_passed = sum(1 for r in model_results_list if r.passed)
            model_stats[model_id] = {
                'total': len(model_results_list),
                'passed': model_passed,
                'pass_rate': model_passed / len(model_results_list) if model_results_list else 0,
                'avg_execution_time': np.mean([r.execution_time_ms for r in model_results_list if r.execution_time_ms]) if model_results_list else 0,
                'error_count': sum(len(r.errors) for r in model_results_list)
            }
        
        # Per-problem statistics
        problem_stats = {}
        for result in results:
            if result.problem_id not in problem_stats:
                problem_stats[result.problem_id] = {
                    'total_samples': 0,
                    'passed_samples': 0,
                    'by_model': {}
                }
            
            stats = problem_stats[result.problem_id]
            stats['total_samples'] += 1
            if result.passed:
                stats['passed_samples'] += 1
            
            if result.model_id not in stats['by_model']:
                stats['by_model'][result.model_id] = {'total': 0, 'passed': 0}
            
            stats['by_model'][result.model_id]['total'] += 1
            if result.passed:
                stats['by_model'][result.model_id]['passed'] += 1
        
        return {
            'summary': summary,
            'model_statistics': model_stats,
            'problem_statistics': problem_stats,
            'detailed_results': [r.to_dict() for r in results[:100]]  # Limit for performance
        }

    def _prepare_comparative_data(
        self,
        evaluations: List[Evaluation],
        results_dict: Dict[str, List[EvaluationResult]],
        benchmark: Optional[Benchmark]
    ) -> Dict[str, Any]:
        """Prepare comparative data"""
        from collections import defaultdict
        
        comparative_data = {
            'evaluations': [],
            'benchmark': benchmark.to_dict() if benchmark else None,
            'model_comparison': {}
        }
        
        # Collect all models
        all_models = set()
        for eval_id, results in results_dict.items():
            for result in results:
                all_models.add(result.model_id)
        
        # Initialize comparison structure
        for model_id in all_models:
            comparative_data['model_comparison'][model_id] = {
                'evaluations': {},
                'aggregate': {
                    'total_results': 0,
                    'passed_results': 0,
                    'avg_execution_time': 0,
                    'metrics': {}
                }
            }
        
        # Aggregate by evaluation
        for eval_id, results in results_dict.items():
            evaluation = next((e for e in evaluations if e.evaluation_id == eval_id), None)
            if evaluation:
                comparative_data['evaluations'].append({
                    'evaluation_id': eval_id,
                    'created_at': evaluation.created_at.isoformat(),
                    'config': evaluation.config
                })
            
            # Group by model for this evaluation
            for result in results:
                model_data = comparative_data['model_comparison'][result.model_id]
                
                # Per-evaluation data
                if eval_id not in model_data['evaluations']:
                    model_data['evaluations'][eval_id] = {
                        'total': 0,
                        'passed': 0,
                        'execution_times': [],
                        'metrics': {}
                    }
                
                eval_stats = model_data['evaluations'][eval_id]
                eval_stats['total'] += 1
                if result.passed:
                    eval_stats['passed'] += 1
                
                if result.execution_time_ms:
                    eval_stats['execution_times'].append(result.execution_time_ms)
                
                # Aggregate metrics
                for name, value in result.metrics.items():
                    if name not in eval_stats['metrics']:
                        eval_stats['metrics'][name] = []
                    eval_stats['metrics'][name].append(value)
        
        # Calculate aggregates
        for model_id, model_data in comparative_data['model_comparison'].items():
            total_results = 0
            passed_results = 0
            all_exec_times = []
            all_metrics = defaultdict(list)
            
            for eval_stats in model_data['evaluations'].values():
                total_results += eval_stats['total']
                passed_results += eval_stats['passed']
                all_exec_times.extend(eval_stats['execution_times'])
                
                for name, values in eval_stats['metrics'].items():
                    all_metrics[name].extend(values)
                
                # Calculate per-evaluation averages
                if eval_stats['total'] > 0:
                    eval_stats['pass_rate'] = eval_stats['passed'] / eval_stats['total']
                    if eval_stats['execution_times']:
                        eval_stats['avg_execution_time'] = np.mean(eval_stats['execution_times'])
                    
                    for name, values in eval_stats['metrics'].items():
                        if values:
                            eval_stats['metrics'][name] = np.mean(values)
            
            # Calculate aggregate
            if total_results > 0:
                model_data['aggregate']['total_results'] = total_results
                model_data['aggregate']['passed_results'] = passed_results
                model_data['aggregate']['pass_rate'] = passed_results / total_results
                if all_exec_times:
                    model_data['aggregate']['avg_execution_time'] = np.mean(all_exec_times)
                
                for name, values in all_metrics.items():
                    if values:
                        model_data['aggregate']['metrics'][name] = np.mean(values)
        
        return comparative_data

    def _generate_summary_charts(
        self,
        results: List[EvaluationResult]
    ) -> Dict[str, Any]:
        """Generate summary charts"""
        charts = {}
        
        # Pass rate pie chart
        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed
        
        if results:
            fig, ax = plt.subplots()
            ax.pie([passed, failed], labels=['Passed', 'Failed'], autopct='%1.1f%%')
            ax.set_title('Overall Pass Rate')
            
            charts['pass_rate_pie'] = self._fig_to_dict(fig)
            plt.close(fig)
        
        # Model performance bar chart
        from collections import defaultdict
        model_results = defaultdict(list)
        for result in results:
            model_results[result.model_id].append(result)
        
        if model_results:
            models = []
            pass_rates = []
            for model_id, model_results_list in model_results.items():
                models.append(model_id)
                model_passed = sum(1 for r in model_results_list if r.passed)
                pass_rates.append(model_passed / len(model_results_list) * 100 if model_results_list else 0)
            
            fig, ax = plt.subplots()
            ax.bar(models, pass_rates)
            ax.set_xlabel('Model')
            ax.set_ylabel('Pass Rate (%)')
            ax.set_title('Model Performance Comparison')
            ax.tick_params(axis='x', rotation=45)
            
            charts['model_performance'] = self._fig_to_dict(fig)
            plt.close(fig)
        
        return charts

    def _generate_detailed_charts(
        self,
        results: List[EvaluationResult]
    ) -> Dict[str, Any]:
        """Generate detailed charts"""
        charts = self._generate_summary_charts(results)
        
        # Execution time histogram
        exec_times = [r.execution_time_ms for r in results if r.execution_time_ms]
        if exec_times:
            fig, ax = plt.subplots()
            ax.hist(exec_times, bins=20)
            ax.set_xlabel('Execution Time (ms)')
            ax.set_ylabel('Frequency')
            ax.set_title('Execution Time Distribution')
            
            charts['execution_time_hist'] = self._fig_to_dict(fig)
            plt.close(fig)
        
        # Error types pie chart
        from collections import defaultdict
        error_types = defaultdict(int)
        for result in results:
            for error in result.errors:
                error_types[error.get('error_type', 'unknown')] += 1
        
        if error_types:
            fig, ax = plt.subplots()
            ax.pie(error_types.values(), labels=error_types.keys(), autopct='%1.1f%%')
            ax.set_title('Error Types Distribution')
            
            charts['error_types'] = self._fig_to_dict(fig)
            plt.close(fig)
        
        return charts

    def _generate_comparative_charts(
        self,
        results_dict: Dict[str, List[EvaluationResult]],
        benchmark: Optional[Benchmark]
    ) -> Dict[str, Any]:
        """Generate comparative charts"""
        charts = {}
        
        # Model ranking chart
        if benchmark and benchmark.rankings:
            models = []
            scores = []
            for model_id, rank in sorted(benchmark.rankings.items(), key=lambda x: x[1]):
                model_info = next((m for m in benchmark.models if m['model_id'] == model_id), {})
                models.append(model_info.get('model_name', model_id))
                scores.append(benchmark.scores.get(model_id, 0))
            
            fig, ax = plt.subplots()
            ax.barh(models, scores)
            ax.set_xlabel('Score')
            ax.set_title('Model Rankings')
            
            charts['model_rankings'] = self._fig_to_dict(fig)
            plt.close(fig)
        
        # Performance over time
        eval_ids = list(results_dict.keys())
        if len(eval_ids) > 1:
            pass_rates = []
            for eval_id in eval_ids:
                results = results_dict[eval_id]
                passed = sum(1 for r in results if r.passed)
                pass_rates.append(passed / len(results) * 100 if results else 0)
            
            fig, ax = plt.subplots()
            ax.plot(range(len(eval_ids)), pass_rates, marker='o')
            ax.set_xlabel('Evaluation')
            ax.set_ylabel('Pass Rate (%)')
            ax.set_title('Performance Trend')
            ax.set_xticks(range(len(eval_ids)))
            ax.set_xticklabels([f'E{i+1}' for i in range(len(eval_ids))])
            
            charts['performance_trend'] = self._fig_to_dict(fig)
            plt.close(fig)
        
        return charts

    def _generate_summary_tables(
        self,
        results: List[EvaluationResult]
    ) -> List[Dict[str, Any]]:
        """Generate summary tables"""
        tables = []
        
        # Model summary table
        from collections import defaultdict
        model_results = defaultdict(list)
        for result in results:
            model_results[result.model_id].append(result)
        
        model_table = {
            'title': 'Model Performance Summary',
            'headers': ['Model', 'Total Samples', 'Passed', 'Failed', 'Pass Rate', 'Avg Time (ms)'],
            'rows': []
        }
        
        for model_id, model_results_list in model_results.items():
            total = len(model_results_list)
            passed = sum(1 for r in model_results_list if r.passed)
            failed = total - passed
            pass_rate = passed / total * 100 if total > 0 else 0
            avg_time = np.mean([r.execution_time_ms for r in model_results_list if r.execution_time_ms]) if model_results_list else 0
            
            model_table['rows'].append([
                model_id,
                str(total),
                str(passed),
                str(failed),
                f"{pass_rate:.1f}%",
                f"{avg_time:.2f}" if avg_time else 'N/A'
            ])
        
        if model_table['rows']:
            tables.append(model_table)
        
        return tables

    def _generate_detailed_tables(
        self,
        results: List[EvaluationResult]
    ) -> List[Dict[str, Any]]:
        """Generate detailed tables"""
        tables = self._generate_summary_tables(results)
        
        # Problem-level table
        from collections import defaultdict
        problem_results = defaultdict(list)
        for result in results:
            problem_results[result.problem_id].append(result)
        
        problem_table = {
            'title': 'Problem-level Results',
            'headers': ['Problem ID', 'Total Samples', 'Passed', 'Failed', 'Pass Rate'],
            'rows': []
        }
        
        for problem_id, problem_results_list in problem_results.items():
            total = len(problem_results_list)
            passed = sum(1 for r in problem_results_list if r.passed)
            failed = total - passed
            pass_rate = passed / total * 100 if total > 0 else 0
            
            problem_table['rows'].append([
                problem_id,
                str(total),
                str(passed),
                str(failed),
                f"{pass_rate:.1f}%"
            ])
        
        if problem_table['rows']:
            tables.append(problem_table)
        
        return tables

    def _generate_comparative_tables(
        self,
        results_dict: Dict[str, List[EvaluationResult]],
        benchmark: Optional[Benchmark]
    ) -> List[Dict[str, Any]]:
        """Generate comparative tables"""
        tables = []
        
        # Benchmark ranking table
        if benchmark:
            ranking_table = {
                'title': 'Benchmark Rankings',
                'headers': ['Rank', 'Model', 'Score', 'Pass@1', 'Pass@5', 'CodeBLEU'],
                'rows': []
            }
            
            sorted_models = sorted(
                benchmark.rankings.items(),
                key=lambda x: x[1]
            )
            
            for model_id, rank in sorted_models:
                model_info = next((m for m in benchmark.models if m['model_id'] == model_id), {})
                model_name = model_info.get('model_name', model_id)
                score = benchmark.scores.get(model_id, 0)
                
                # Get metrics
                metrics = benchmark.results.get(model_id, {})
                pass1 = metrics.get('pass@1', 0) * 100
                pass5 = metrics.get('pass@5', 0) * 100
                codebleu = metrics.get('codebleu', 0) * 100
                
                ranking_table['rows'].append([
                    str(rank),
                    model_name,
                    f"{score:.3f}",
                    f"{pass1:.1f}%",
                    f"{pass5:.1f}%",
                    f"{codebleu:.1f}%"
                ])
            
            if ranking_table['rows']:
                tables.append(ranking_table)
        
        # Cross-evaluation comparison table
        if len(results_dict) > 1:
            comparison_table = {
                'title': 'Cross-Evaluation Comparison',
                'headers': ['Model'] + [f'Eval {i+1}' for i in range(len(results_dict))] + ['Average'],
                'rows': []
            }
            
            # Collect all models
            all_models = set()
            for results in results_dict.values():
                for result in results:
                    all_models.add(result.model_id)
            
            for model_id in sorted(all_models):
                row = [model_id]
                pass_rates = []
                
                for eval_id, results in results_dict.items():
                    model_results = [r for r in results if r.model_id == model_id]
                    if model_results:
                        passed = sum(1 for r in model_results if r.passed)
                        pass_rate = passed / len(model_results) * 100
                        pass_rates.append(pass_rate)
                        row.append(f"{pass_rate:.1f}%")
                    else:
                        row.append('N/A')
                
                if pass_rates:
                    avg_pass = np.mean(pass_rates)
                    row.append(f"{avg_pass:.1f}%")
                else:
                    row.append('N/A')
                
                comparison_table['rows'].append(row)
            
            if comparison_table['rows']:
                tables.append(comparison_table)
        
        return tables

    def _fig_to_dict(self, fig: plt.Figure) -> Dict[str, Any]:
        """Convert matplotlib figure to dict for serialization"""
        import io
        import base64
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        
        return {
            'image': img_str,
            'format': 'png'
        }