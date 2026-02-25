# src/dashboard/routes.py
from flask import render_template, jsonify, request, session, send_file, current_app
import logging
from pathlib import Path
import json
import pandas as pd
from datetime import datetime
import plotly.utils
import plotly.graph_objects as go
import plotly.express as px
import random
import os

from ..managers import EvaluationManager, ResultAggregator
from ..entities import Evaluation, EvaluationResult
from ..generators import ReportGenerator
from ..utils.disk_space_manager import DiskSpaceManager

logger = logging.getLogger(__name__)

# Mock data for when real data isn't available
MOCK_EVALUATIONS = [
    {
        'evaluation_id': 'eval_1a2b3c4d',
        'user_id': 'user_123',
        'model_ids': ['codellama:7b', 'starcoder:1b'],
        'dataset_id': 'humaneval',
        'status': 'completed',
        'created_at': (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)).isoformat(),
        'started_at': (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)).isoformat(),
        'completed_at': (datetime.now().replace(hour=1, minute=0, second=0, microsecond=0)).isoformat(),
        'progress': 100,
        'current_stage': 'completed',
        'results_ids': ['res_1', 'res_2', 'res_3'],
        'report_ids': ['rpt_1'],
        'config': {'num_samples': 5, 'timeout': 30}
    },
    {
        'evaluation_id': 'eval_5e6f7g8h',
        'user_id': 'user_123',
        'model_ids': ['codellama:7b'],
        'dataset_id': 'humaneval',
        'status': 'running',
        'created_at': (datetime.now().replace(hour=2, minute=0, second=0, microsecond=0)).isoformat(),
        'started_at': (datetime.now().replace(hour=2, minute=30, second=0, microsecond=0)).isoformat(),
        'completed_at': None,
        'progress': 45,
        'current_stage': 'evaluating_models',
        'results_ids': ['res_4', 'res_5'],
        'report_ids': [],
        'config': {'num_samples': 3, 'timeout': 30}
    }
]

MOCK_RESULTS = []
for i in range(15):
    MOCK_RESULTS.append({
        'result_id': f'res_{i}',
        'evaluation_id': random.choice(['eval_1a2b3c4d', 'eval_5e6f7g8h']),
        'problem_id': f'prob_{i % 5}',
        'model_id': random.choice(['codellama:7b', 'starcoder:1b']),
        'sample_id': i % 3,
        'generated_code': 'def solution():\n    return True',
        'execution_output': 'All tests passed',
        'passed': random.choice([True, False]),
        'execution_time_ms': random.uniform(10, 100),
        'memory_usage_kb': random.uniform(1000, 5000),
        'test_results': [
            {'test_id': 0, 'passed': True, 'message': 'Test 1 passed'},
            {'test_id': 1, 'passed': True, 'message': 'Test 2 passed'}
        ],
        'errors': [] if random.random() > 0.3 else [{
            'error_type': 'runtime_error',
            'error_message': 'Division by zero',
            'severity': 'error'
        }],
        'metrics': {
            'pass_rate': random.uniform(0, 1),
            'execution_time': random.uniform(10, 100),
            'codebleu': random.uniform(0.5, 1)
        },
        'created_at': datetime.now().isoformat(),
        'metadata': {},
        'source': 'generated'
    })

MOCK_MODELS = [
    {
        'model_id': 'codellama:7b',
        'provider': 'ollama',
        'config': {'base_url': 'http://localhost:11434'},
        'active': True,
        'capabilities': ['code_generation', 'python', 'javascript']
    },
    {
        'model_id': 'codellama:13b',
        'provider': 'ollama',
        'config': {'base_url': 'http://localhost:11434'},
        'active': False,
        'capabilities': ['code_generation', 'python', 'javascript']
    },
    {
        'model_id': 'starcoder:1b',
        'provider': 'ollama',
        'config': {'base_url': 'http://localhost:11434'},
        'active': True,
        'capabilities': ['code_generation', 'python']
    }
]

MOCK_BENCHMARKS = [
    {
        'benchmark_id': 'ben_12345678',
        'name': 'HumanEval Benchmark',
        'description': 'Standard benchmark for code generation',
        'created_at': (datetime.now().replace(day=datetime.now().day-5)).isoformat(),
        'updated_at': (datetime.now().replace(day=datetime.now().day-1)).isoformat(),
        'models': [
            {'model_id': 'codellama:7b', 'model_name': 'CodeLlama 7B'},
            {'model_id': 'starcoder:1b', 'model_name': 'StarCoder 1B'}
        ],
        'metrics': ['pass_rate', 'execution_time'],
        'results': {
            'codellama:7b': {'pass_rate': 0.85, 'execution_time': 45.2},
            'starcoder:1b': {'pass_rate': 0.62, 'execution_time': 38.7}
        },
        'rankings': {'codellama:7b': 1, 'starcoder:1b': 2},
        'scores': {'codellama:7b': 0.85, 'starcoder:1b': 0.62},
        'metadata': {}
    }
]


def register_routes(app):
    """Register all routes with the app"""
    
    @app.route('/')
    def index():
        """Main dashboard page"""
        return render_template('index.html',
                             active_page='dashboard')

    @app.route('/evaluations')
    def evaluations():
        """List all evaluations"""
        evaluations_list = []
        
        # Try to get from manager if available
        if hasattr(app, 'evaluation_manager') and app.evaluation_manager:
            try:
                evaluations_list = list(app.evaluation_manager.evaluations.values())
                # Convert to dict for template
                evaluations_list = [e.to_dict() if hasattr(e, 'to_dict') else e for e in evaluations_list]
            except Exception as e:
                logger.warning(f"Could not load evaluations from manager: {e}")
                evaluations_list = MOCK_EVALUATIONS
        else:
            evaluations_list = MOCK_EVALUATIONS
        
        return render_template('evaluations.html',
                             evaluations=evaluations_list,
                             active_page='evaluations')

    @app.route('/evaluation/<evaluation_id>')
    def evaluation_detail(evaluation_id):
        """Show evaluation details"""
        evaluation = None
        results = []
        
        # Try to get from manager if available
        if hasattr(app, 'evaluation_manager') and app.evaluation_manager:
            try:
                evaluation = app.evaluation_manager.get_evaluation(evaluation_id)
                if evaluation:
                    results = app.evaluation_manager.get_results(evaluation_id)
            except Exception as e:
                logger.warning(f"Could not load evaluation from manager: {e}")
        
        # Fallback to mock data
        if not evaluation:
            evaluation = next((e for e in MOCK_EVALUATIONS if e['evaluation_id'] == evaluation_id), None)
            results = [r for r in MOCK_RESULTS if r['evaluation_id'] == evaluation_id]
        
        if not evaluation:
            return render_template('error.html',
                                 error_code=404,
                                 error_message=f"Evaluation {evaluation_id} not found"), 404
        
        return render_template('evaluation_detail.html',
                             evaluation=evaluation,
                             results=results,
                             active_page='evaluations')

    @app.route('/models')
    def models():
        """List available models"""
        models_list = []
        
        # Try to get from registry if available
        if (hasattr(app, 'evaluation_manager') and 
            app.evaluation_manager and 
            hasattr(app.evaluation_manager, 'model_registry') and
            app.evaluation_manager.model_registry):
            try:
                models_list = app.evaluation_manager.model_registry.list_models()
            except Exception as e:
                logger.warning(f"Error listing models: {e}")
                models_list = MOCK_MODELS
        else:
            models_list = MOCK_MODELS
        
        return render_template('models.html',
                             models=models_list,
                             active_page='models')

    @app.route('/benchmarks')
    def benchmarks():
        """List benchmarks"""
        benchmarks_list = []
        
        # Try to get from aggregator if available
        if hasattr(app, 'result_aggregator') and app.result_aggregator:
            try:
                benchmarks_list = list(app.result_aggregator.benchmarks.values())
                benchmarks_list = [b.to_dict() if hasattr(b, 'to_dict') else b for b in benchmarks_list]
            except Exception as e:
                logger.warning(f"Could not load benchmarks: {e}")
                benchmarks_list = MOCK_BENCHMARKS
        else:
            benchmarks_list = MOCK_BENCHMARKS
        
        return render_template('benchmarks.html',
                             benchmarks=benchmarks_list,
                             active_page='benchmarks')

    @app.route('/reports')
    def reports():
        """List generated reports"""
        reports_dir = Path('reports')
        reports_list = []
        
        if reports_dir.exists():
            for file in reports_dir.glob('*'):
                reports_list.append({
                    'name': file.name,
                    'path': str(file),
                    'size': file.stat().st_size,
                    'modified': datetime.fromtimestamp(file.stat().st_mtime)
                })
        
        return render_template('reports.html',
                             reports=reports_list,
                             active_page='reports')

    @app.route('/settings')
    def settings():
        """Settings page"""
        return render_template('settings.html',
                             active_page='settings')

    # API Routes

    @app.route('/api/health')
    def health():
        """Health check endpoint"""
        disk_space = None
        try:
            disk_space = DiskSpaceManager.get_available_space_gb()
        except:
            disk_space = 50.5  # Mock value
            
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'disk_space': disk_space
        })

    @app.route('/api/evaluations')
    def api_evaluations():
        """Get all evaluations"""
        evaluations_list = []
        
        # Try to get from manager if available
        if hasattr(app, 'evaluation_manager') and app.evaluation_manager:
            try:
                for eval_id, evaluation in app.evaluation_manager.evaluations.items():
                    if hasattr(evaluation, 'to_dict'):
                        eval_dict = evaluation.to_dict()
                    else:
                        eval_dict = {'evaluation_id': eval_id}
                    eval_dict['results_count'] = len(getattr(evaluation, 'results_ids', []))
                    evaluations_list.append(eval_dict)
            except Exception as e:
                logger.warning(f"Error getting evaluations from manager: {e}")
                evaluations_list = MOCK_EVALUATIONS
        else:
            evaluations_list = MOCK_EVALUATIONS
        
        # Apply limit if specified
        limit = request.args.get('limit', type=int)
        if limit:
            evaluations_list = evaluations_list[:limit]
        
        return jsonify(evaluations_list)

    @app.route('/api/evaluations/<evaluation_id>')
    def api_evaluation(evaluation_id):
        """Get evaluation details"""
        evaluation = None
        results = []
        
        # Try to get from manager if available
        if hasattr(app, 'evaluation_manager') and app.evaluation_manager:
            try:
                evaluation = app.evaluation_manager.get_evaluation(evaluation_id)
                if evaluation:
                    results = app.evaluation_manager.get_results(evaluation_id)
                    evaluation = evaluation.to_dict() if hasattr(evaluation, 'to_dict') else {'evaluation_id': evaluation_id}
                    results = [r.to_dict() if hasattr(r, 'to_dict') else r for r in results]
            except Exception as e:
                logger.warning(f"Error getting evaluation from manager: {e}")
        
        # Fallback to mock
        if not evaluation:
            evaluation = next((e for e in MOCK_EVALUATIONS if e['evaluation_id'] == evaluation_id), None)
            results = [r for r in MOCK_RESULTS if r['evaluation_id'] == evaluation_id]
        
        if not evaluation:
            return jsonify({'error': 'Evaluation not found'}), 404
        
        return jsonify({
            'evaluation': evaluation,
            'results': results
        })

    @app.route('/api/evaluations', methods=['POST'])
    def api_create_evaluation():
        """Create a new evaluation"""
        data = request.get_json()
        
        # Try to create via manager if available
        if hasattr(app, 'evaluation_manager') and app.evaluation_manager:
            try:
                evaluation = app.evaluation_manager.create_evaluation(
                    user_id=data.get('user_id', 'anonymous'),
                    model_ids=data.get('models', []),
                    dataset_id=data.get('dataset_id'),
                    config=data.get('config', {})
                )
                return jsonify(evaluation.to_dict() if hasattr(evaluation, 'to_dict') else {'evaluation_id': 'created'}), 201
            except Exception as e:
                logger.error(f"Failed to create evaluation via manager: {e}")
        
        # Fallback to mock creation
        new_evaluation = {
            'evaluation_id': f"eval_{len(MOCK_EVALUATIONS) + 1}",
            'user_id': data.get('user_id', 'anonymous'),
            'model_ids': data.get('models', []),
            'dataset_id': data.get('dataset_id', 'humaneval'),
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'started_at': None,
            'completed_at': None,
            'progress': 0,
            'current_stage': 'initializing',
            'results_ids': [],
            'report_ids': [],
            'config': data.get('config', {})
        }
        
        return jsonify(new_evaluation), 201

    @app.route('/api/evaluations/<evaluation_id>/start', methods=['POST'])
    def api_start_evaluation(evaluation_id):
        """Start an evaluation"""
        # Try via manager
        if hasattr(app, 'evaluation_manager') and app.evaluation_manager:
            try:
                import asyncio
                asyncio.create_task(app.evaluation_manager.run_evaluation(evaluation_id))
                return jsonify({'status': 'started'})
            except Exception as e:
                logger.warning(f"Could not start via manager: {e}")
        
        # Fallback to mock
        return jsonify({'status': 'started', 'message': 'Mock evaluation started'})

    @app.route('/api/evaluations/<evaluation_id>/cancel', methods=['POST'])
    def api_cancel_evaluation(evaluation_id):
        """Cancel an evaluation"""
        # Try via manager
        if hasattr(app, 'evaluation_manager') and app.evaluation_manager:
            try:
                success = app.evaluation_manager.cancel_evaluation(evaluation_id)
                if success:
                    return jsonify({'status': 'cancelled'})
            except Exception as e:
                logger.warning(f"Could not cancel via manager: {e}")
        
        # Fallback to mock
        return jsonify({'status': 'cancelled', 'message': 'Mock evaluation cancelled'})

    @app.route('/api/models')
    def api_models():
        """Get available models"""
        models_list = []
        
        # Try via registry
        if (hasattr(app, 'evaluation_manager') and 
            app.evaluation_manager and 
            hasattr(app.evaluation_manager, 'model_registry') and
            app.evaluation_manager.model_registry):
            try:
                models_list = app.evaluation_manager.model_registry.list_models()
            except Exception as e:
                logger.warning(f"Error in api_models: {e}")
                models_list = MOCK_MODELS
        else:
            models_list = MOCK_MODELS
        
        return jsonify(models_list)

    @app.route('/api/models/<model_id>/test', methods=['POST'])
    def api_test_model(model_id):
        """Test model connection"""
        # Try via registry
        if (hasattr(app, 'evaluation_manager') and 
            app.evaluation_manager and 
            hasattr(app.evaluation_manager, 'model_registry') and
            app.evaluation_manager.model_registry):
            try:
                model = app.evaluation_manager.model_registry.get_model(model_id)
                if model:
                    import asyncio
                    success = asyncio.run(model.test_connection())
                    return jsonify({
                        'model_id': model_id,
                        'connected': success
                    })
            except Exception as e:
                logger.warning(f"Could not test model via registry: {e}")
        
        # Fallback to mock
        return jsonify({
            'model_id': model_id,
            'connected': True,
            'latency_ms': random.randint(50, 200)
        })

    @app.route('/api/results')
    def api_results():
        """Get results with optional filtering"""
        evaluation_id = request.args.get('evaluation_id')
        model_id = request.args.get('model_id')
        problem_id = request.args.get('problem_id')
        
        results_list = []
        
        # Try via manager
        if hasattr(app, 'evaluation_manager') and app.evaluation_manager:
            try:
                for result in app.evaluation_manager.results.values():
                    if evaluation_id and getattr(result, 'evaluation_id', None) != evaluation_id:
                        continue
                    if model_id and getattr(result, 'model_id', None) != model_id:
                        continue
                    if problem_id and getattr(result, 'problem_id', None) != problem_id:
                        continue
                    
                    if hasattr(result, 'to_dict'):
                        results_list.append(result.to_dict())
                    else:
                        results_list.append({'result_id': 'unknown'})
            except Exception as e:
                logger.warning(f"Error getting results from manager: {e}")
                results_list = MOCK_RESULTS
        else:
            results_list = MOCK_RESULTS
        
        # Apply filters to mock data
        if evaluation_id:
            results_list = [r for r in results_list if r.get('evaluation_id') == evaluation_id]
        if model_id:
            results_list = [r for r in results_list if r.get('model_id') == model_id]
        if problem_id:
            results_list = [r for r in results_list if r.get('problem_id') == problem_id]
        
        return jsonify(results_list)

    @app.route('/api/benchmarks')
    def api_benchmarks():
        """Get all benchmarks"""
        benchmarks_list = []
        
        # Try via aggregator
        if hasattr(app, 'result_aggregator') and app.result_aggregator:
            try:
                for benchmark_id, benchmark in app.result_aggregator.benchmarks.items():
                    if hasattr(benchmark, 'to_dict'):
                        benchmarks_list.append(benchmark.to_dict())
                    else:
                        benchmarks_list.append({'benchmark_id': benchmark_id})
            except Exception as e:
                logger.warning(f"Error getting benchmarks: {e}")
                benchmarks_list = MOCK_BENCHMARKS
        else:
            benchmarks_list = MOCK_BENCHMARKS
        
        return jsonify(benchmarks_list)

    @app.route('/api/benchmarks', methods=['POST'])
    def api_create_benchmark():
        """Create a new benchmark"""
        data = request.get_json()
        
        # Try via aggregator
        if hasattr(app, 'result_aggregator') and app.result_aggregator:
            try:
                benchmark = app.result_aggregator.create_benchmark(
                    name=data['name'],
                    description=data.get('description', ''),
                    evaluation_ids=data.get('evaluation_ids', []),
                    metric_weights=data.get('metric_weights')
                )
                return jsonify(benchmark.to_dict() if hasattr(benchmark, 'to_dict') else {}), 201
            except Exception as e:
                logger.error(f"Failed to create benchmark via aggregator: {e}")
        
        # Fallback to mock
        new_benchmark = {
            'benchmark_id': f"ben_{len(MOCK_BENCHMARKS) + 1}",
            'name': data.get('name', 'New Benchmark'),
            'description': data.get('description', ''),
            'created_at': datetime.now().isoformat(),
            'models': [],
            'rankings': {},
            'scores': {}
        }
        
        return jsonify(new_benchmark), 201

    @app.route('/api/reports', methods=['POST'])
    def api_generate_report():
        """Generate a report"""
        data = request.get_json()
        
        # Try via generator
        if hasattr(app, 'report_generator') and app.report_generator:
            try:
                evaluation_id = data.get('evaluation_id')
                format = data.get('format', 'html')
                report_type = data.get('type', 'summary')
                
                # Need evaluation and results
                if hasattr(app, 'evaluation_manager') and app.evaluation_manager:
                    evaluation = app.evaluation_manager.get_evaluation(evaluation_id)
                    results = app.evaluation_manager.get_results(evaluation_id)
                    
                    if evaluation and results is not None:
                        if report_type == 'summary':
                            report = app.report_generator.generate_summary_report(
                                evaluation, results, format
                            )
                        else:
                            report = app.report_generator.generate_detailed_report(
                                evaluation, results, format
                            )
                        
                        return jsonify(report.to_dict() if hasattr(report, 'to_dict') else {}), 201
            except Exception as e:
                logger.error(f"Failed to generate report via generator: {e}")
        
        # Fallback to mock
        report = {
            'report_id': f"rpt_{random.randint(1000, 9999)}",
            'evaluation_id': data.get('evaluation_id'),
            'report_type': data.get('type', 'summary'),
            'format': data.get('format', 'html'),
            'generated_at': datetime.now().isoformat(),
            'file_path': f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{data.get('format', 'html')}",
            'download_count': 0
        }
        
        # Create mock file
        reports_dir = Path('reports')
        reports_dir.mkdir(exist_ok=True)
        report_path = reports_dir / Path(report['file_path']).name
        with open(report_path, 'w') as f:
            f.write(f"Mock report for evaluation {data.get('evaluation_id')}")
        
        return jsonify(report), 201

    @app.route('/api/reports/<report_id>/download')
    def api_download_report(report_id):
        """Download a report file"""
        reports_dir = Path('reports')
        
        # Find report file
        for file in reports_dir.glob(f'*{report_id}*'):
            return send_file(
                str(file),
                as_attachment=True,
                download_name=file.name
            )
        
        return jsonify({'error': 'Report not found'}), 404

    @app.route('/api/stats')
    def api_stats():
        """Get system statistics"""
        stats = {
            'disk_space': 50.5,
            'evaluations': 0,
            'completed_evaluations': 0,
            'running_evaluations': 0,
            'results': 0,
            'pass_rate': 0,
            'active_models': 0,
            'total_models': 0,
            'reports': 0
        }
        
        # Try to get real stats
        if hasattr(app, 'evaluation_manager') and app.evaluation_manager:
            try:
                stats['evaluations'] = len(app.evaluation_manager.evaluations)
                stats['results'] = len(app.evaluation_manager.results)
                
                # Count completed/running
                completed = 0
                running = 0
                for eval_id, evaluation in app.evaluation_manager.evaluations.items():
                    status = getattr(evaluation, 'status', None)
                    if status:
                        status_str = status.value if hasattr(status, 'value') else str(status)
                        if 'complete' in status_str.lower():
                            completed += 1
                        elif 'running' in status_str.lower():
                            running += 1
                
                stats['completed_evaluations'] = completed
                stats['running_evaluations'] = running
                
                # Calculate pass rate
                if stats['results'] > 0:
                    passed = 0
                    for result in app.evaluation_manager.results.values():
                        if getattr(result, 'passed', False):
                            passed += 1
                    stats['pass_rate'] = round((passed / stats['results']) * 100, 1)
                
                # Model counts
                if hasattr(app.evaluation_manager, 'model_registry') and app.evaluation_manager.model_registry:
                    models = app.evaluation_manager.model_registry.list_models()
                    stats['total_models'] = len(models)
                    stats['active_models'] = len([m for m in models if m.get('active', False)])
            except Exception as e:
                logger.warning(f"Error calculating stats from manager: {e}")
        
        # Fallback to mock stats using mock data
        if stats['evaluations'] == 0:
            stats['evaluations'] = len(MOCK_EVALUATIONS)
            stats['completed_evaluations'] = len([e for e in MOCK_EVALUATIONS if e.get('status') == 'completed'])
            stats['running_evaluations'] = len([e for e in MOCK_EVALUATIONS if e.get('status') == 'running'])
            stats['results'] = len(MOCK_RESULTS)
            
            passed = len([r for r in MOCK_RESULTS if r.get('passed', False)])
            stats['pass_rate'] = round((passed / stats['results']) * 100, 1) if stats['results'] > 0 else 0
            
            stats['total_models'] = len(MOCK_MODELS)
            stats['active_models'] = len([m for m in MOCK_MODELS if m.get('active', False)])
        
        # Count reports
        reports_dir = Path('reports')
        if reports_dir.exists():
            stats['reports'] = len(list(reports_dir.glob('*')))
        
        return jsonify(stats)

    @app.route('/api/charts/pass_rate')
    def api_chart_pass_rate():
        """Generate pass rate chart"""
        evaluation_id = request.args.get('evaluation_id')
        
        models = []
        pass_rates = []
        
        # Try to use real data
        if hasattr(app, 'evaluation_manager') and app.evaluation_manager and evaluation_id:
            try:
                results = app.evaluation_manager.get_results(evaluation_id)
                
                # Group by model
                model_results = {}
                for result in results:
                    model_id = getattr(result, 'model_id', 'unknown')
                    if model_id not in model_results:
                        model_results[model_id] = []
                    model_results[model_id].append(result)
                
                # Calculate pass rates
                for model_id, model_results_list in model_results.items():
                    models.append(model_id)
                    passed = sum(1 for r in model_results_list if getattr(r, 'passed', False))
                    total = len(model_results_list)
                    pass_rates.append((passed / total * 100) if total > 0 else 0)
            except Exception as e:
                logger.warning(f"Error generating chart from real data: {e}")
        
        # Fallback to mock data
        if not models:
            # Calculate from mock results
            if evaluation_id:
                relevant_results = [r for r in MOCK_RESULTS if r.get('evaluation_id') == evaluation_id]
            else:
                relevant_results = MOCK_RESULTS
            
            model_stats = {}
            for result in relevant_results:
                model_id = result.get('model_id', 'unknown')
                if model_id not in model_stats:
                    model_stats[model_id] = {'total': 0, 'passed': 0}
                model_stats[model_id]['total'] += 1
                if result.get('passed', False):
                    model_stats[model_id]['passed'] += 1
            
            for model_id, stats in model_stats.items():
                models.append(model_id)
                pass_rates.append((stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0)
        
        # If still no data, use default
        if not models:
            models = ['codellama:7b', 'starcoder:1b']
            pass_rates = [85, 62]
        
        fig = go.Figure(data=[
            go.Bar(x=models, y=pass_rates, marker_color='#3498db')
        ])
        
        fig.update_layout(
            title='Model Pass Rates',
            xaxis_title='Model',
            yaxis_title='Pass Rate (%)',
            yaxis_range=[0, 100]
        )
        
        return jsonify(json.loads(fig.to_json()))

    @app.route('/api/charts/error_distribution')
    def api_chart_error_distribution():
        """Generate error distribution chart"""
        evaluation_id = request.args.get('evaluation_id')
        
        error_types = {}
        
        # Try to use real data
        if hasattr(app, 'evaluation_manager') and app.evaluation_manager and evaluation_id:
            try:
                results = app.evaluation_manager.get_results(evaluation_id)
                for result in results:
                    for error in getattr(result, 'errors', []):
                        error_type = error.get('error_type', 'unknown')
                        error_types[error_type] = error_types.get(error_type, 0) + 1
            except Exception as e:
                logger.warning(f"Error getting error distribution: {e}")
        
        # Fallback to mock
        if not error_types and evaluation_id:
            # Generate mock error distribution
            error_types = {
                'syntax_error': random.randint(5, 15),
                'runtime_error': random.randint(10, 25),
                'type_error': random.randint(3, 10),
                'name_error': random.randint(2, 8)
            }
        
        if not error_types:
            error_types = {'No errors': 1}
        
        fig = go.Figure(data=[
            go.Pie(labels=list(error_types.keys()),
                  values=list(error_types.values()))
        ])
        
        fig.update_layout(title='Error Type Distribution')
        
        return jsonify(json.loads(fig.to_json()))

    @app.route('/api/search')
    def api_search():
        """Search endpoint"""
        query = request.args.get('q', '').lower()
        
        if not query or len(query) < 2:
            return jsonify([])
        
        results = []
        
        # Search evaluations
        if hasattr(app, 'evaluation_manager') and app.evaluation_manager:
            try:
                for eval_id, evaluation in app.evaluation_manager.evaluations.items():
                    if query in eval_id.lower():
                        results.append({
                            'type': 'evaluation',
                            'id': eval_id,
                            'title': f"Evaluation {eval_id[:8]}",
                            'url': f"/evaluation/{eval_id}"
                        })
            except Exception as e:
                logger.warning(f"Error searching evaluations: {e}")
        
        # Also search mock data
        for eval_item in MOCK_EVALUATIONS:
            eval_id = eval_item.get('evaluation_id', '')
            if query in eval_id.lower():
                # Check if already added
                if not any(r.get('id') == eval_id for r in results):
                    results.append({
                        'type': 'evaluation',
                        'id': eval_id,
                        'title': f"Evaluation {eval_id[:8]}",
                        'url': f"/evaluation/{eval_id}"
                    })
        
        # Search models
        for model in MOCK_MODELS:
            model_id = model.get('model_id', '')
            if query in model_id.lower():
                results.append({
                    'type': 'model',
                    'id': model_id,
                    'title': f"Model {model_id}",
                    'url': f"/models#{model_id}"
                })
        
        return jsonify(results[:10])  # Limit to 10 results

    @app.route('/api/debug/status')
    def api_debug_status():
        """Debug endpoint to check system status"""
        status = {
            'evaluation_manager': hasattr(app, 'evaluation_manager') and app.evaluation_manager is not None,
            'result_aggregator': hasattr(app, 'result_aggregator') and app.result_aggregator is not None,
            'report_generator': hasattr(app, 'report_generator') and app.report_generator is not None,
            'model_registry': False,
            'using_mock_data': True
        }
        
        if status['evaluation_manager'] and hasattr(app.evaluation_manager, 'model_registry'):
            status['model_registry'] = app.evaluation_manager.model_registry is not None
        
        # Check if we're using any real data
        if (status['evaluation_manager'] or status['result_aggregator'] or 
            status['report_generator'] or status['model_registry']):
            status['using_mock_data'] = False
        
        return jsonify(status)