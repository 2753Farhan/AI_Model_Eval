from venv import logger
from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import os
import gzip
from pathlib import Path
import plotly.express as px
import plotly.utils

app = Flask(__name__)




class DashboardDataManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.metrics_df = None
        self.samples_data = None
        self.evaluation_results = None
        self.load_data()
    
    def load_data(self):
        """Load all data for enhanced dashboard"""
        try:
            # Load baseline metrics
            metrics_path = self.base_dir / "results" / "human_baseline_metrics.csv"
            if metrics_path.exists():
                self.metrics_df = pd.read_csv(metrics_path)
                print(f"✅ Loaded baseline metrics for {len(self.metrics_df)} problems")
            
            # Load evaluation results
            results_path = self.base_dir / "results" / "evaluation_results.csv"
            if results_path.exists():
                self.evaluation_results = pd.read_csv(results_path)
                print(f"✅ Loaded evaluation results for {len(self.evaluation_results)} samples")
            
            # Load original dataset
            dataset_path = self.base_dir / "data" / "human_eval_repo" / "data" / "HumanEval.jsonl.gz"
            if dataset_path.exists():
                self.samples_data = []
                with gzip.open(dataset_path, 'rt', encoding='utf-8') as f:
                    for line in f:
                        self.samples_data.append(json.loads(line))
                print(f"✅ Loaded {len(self.samples_data)} original problems")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def get_problem_details(self, problem_id):
        """Get complete details for a problem with enhanced info."""
        print(f"Fetching details for problem: {problem_id}")
        print(f"Metrics DataFrame columns: {self.metrics_df.columns.tolist() if self.metrics_df is not None else 'No metrics loaded'}")
        if self.metrics_df is None or self.samples_data is None:
            return None
        
        # Find metrics
        metrics_row = self.metrics_df[self.metrics_df['problem_id'] == problem_id]
        if metrics_row.empty:
            return None

        # Find original data
        original_data = next((item for item in self.samples_data if item['task_id'] == problem_id), None)
        if not original_data:
            return None
        
        # Extract function name from prompt
        prompt = original_data.get('prompt', '')
        function_name = "Unknown"
        if 'def ' in prompt:
            function_name = prompt.split('def ')[1].split('(')[0].strip()
        
        # Calculate additional metrics
        loc = metrics_row.iloc[0].get('loc')
        comments = metrics_row.iloc[0].get('comments')
        comment_ratio = None
        if loc and comments:
            comment_ratio = (comments / loc) * 100
        
        # Combine data
        problem_data = {
            'problem_id': problem_id,
            'function_name': function_name,
            'prompt': original_data.get('prompt', ''),
            'canonical_solution': original_data.get('canonical_solution', ''),
            'test': original_data.get('test', ''),
            'entry_point': original_data.get('entry_point', ''),
            'metrics': metrics_row.iloc[0].to_dict(),
            'additional_metrics': {
                'comment_ratio': comment_ratio,
                'function_name': function_name
            }
        }
        
        return problem_data
    
    def get_all_problems(self):
        """Get all problems with basic info."""
        if self.metrics_df is None or self.samples_data is None:
            return []
        
        problems = []
        for _, row in self.metrics_df.iterrows():
            problem_id = row['problem_id']
            original_data = next((item for item in self.samples_data if item['task_id'] == problem_id), None)
            
            if original_data:
                # Extract function name from prompt
                prompt = original_data.get('prompt', '')
                function_name = "Unknown"
                if 'def ' in prompt:
                    function_name = prompt.split('def ')[1].split('(')[0].strip()
                
                problems.append({
                    'problem_id': problem_id,
                    'function_name': function_name,
                    'prompt_preview': prompt[:80] + '...' if len(prompt) > 80 else prompt,
                    'loc': row.get('loc'),
                    'lloc': row.get('lloc'),
                    'comments': row.get('comments'),
                    'cyclomatic_complexity': row.get('cyclomatic_complexity'),
                    'maintainability_index': row.get('maintainability_index'),
                    'cognitive_complexity': row.get('cognitive_complexity'),
                    'pylint_errors': row.get('pylint_errors'),
                    'pylint_warnings': row.get('pylint_warnings'),
                    'security_issues': row.get('security_issues')
                })
        
        return problems

    def get_metrics_summary(self):
        """Get summary statistics for metrics."""
        if self.metrics_df is None:
            return {}
        
        numeric_cols = self.metrics_df.select_dtypes(include=['number']).columns
        summary = {}
        
        for col in numeric_cols:
            valid_data = self.metrics_df[col].dropna()
            if len(valid_data) > 0:
                summary[col] = {
                    'mean': round(valid_data.mean(), 2),
                    'std': round(valid_data.std(), 2),
                    'min': round(valid_data.min(), 2),
                    'max': round(valid_data.max(), 2),
                    'count': len(valid_data)
                }
        
        return summary

# Initialize data manager
data_manager = DashboardDataManager()

# Add custom Jinja2 filter for clamping values
def clamp_filter(value, min_val, max_val):
    """Clamp a value between min and max."""
    return max(min_val, min(value, max_val))

app.jinja_env.filters['clamp'] = clamp_filter

@app.route('/')
def index():
    """Main dashboard page."""
    problems = data_manager.get_all_problems()
    summary = data_manager.get_metrics_summary()
    
    return render_template('index.html', 
                         problems=problems, 
                         summary=summary,
                         total_problems=len(problems))

@app.route('/problem/<int:problem_number>')
def problem_detail(problem_number):
    """Problem detail page with code and metrics."""
    problem_id = f"HumanEval/{problem_number}"
    problem_data = data_manager.get_problem_details(problem_id)
    
    if not problem_data:
        return f"Problem {problem_id} not found", 404
    
    return render_template('problem_detail.html', problem=problem_data)

@app.route('/metrics')
def metrics_overview():
    """Metrics visualization page."""
    if data_manager.metrics_df is None:
        return "No data available", 404
    
    # Get metrics summary
    summary = data_manager.get_metrics_summary()
    
    # Create charts data
    charts_data = {}
    
    # LOC Distribution
    if 'loc' in data_manager.metrics_df.columns:
        fig_loc = px.histogram(data_manager.metrics_df, x='loc', 
                              title='Lines of Code Distribution',
                              nbins=20)
        charts_data['loc_chart'] = fig_loc.to_json()
    
    # Complexity vs Maintainability
    if all(col in data_manager.metrics_df.columns for col in ['cyclomatic_complexity', 'maintainability_index']):
        fig_scatter = px.scatter(data_manager.metrics_df, 
                               x='cyclomatic_complexity', 
                               y='maintainability_index',
                               title='Complexity vs Maintainability',
                               hover_data=['problem_id'])
        charts_data['scatter_chart'] = fig_scatter.to_json()
    
    # Cognitive Complexity
    if 'cognitive_complexity' in data_manager.metrics_df.columns:
        fig_cog = px.box(data_manager.metrics_df, y='cognitive_complexity',
                        title='Cognitive Complexity Distribution')
        charts_data['cog_chart'] = fig_cog.to_json()
    
    return render_template('metrics.html', charts_data=charts_data, summary=summary)

@app.route('/api/metrics/chart')
def api_metrics_chart():
    """API endpoint for metrics charts."""
    print(f"📊 API Chart request: {request.args.get('type')}")
    
    if data_manager.metrics_df is None:
        print("❌ No metrics data available")
        return jsonify({'error': 'No data available. Run baseline analysis first.'}), 404
    
    chart_type = request.args.get('type', 'loc_distribution')
    print(f"📈 Processing chart type: {chart_type}")
    
    try:
        if chart_type == 'loc_distribution':
            print("📍 Processing LOC distribution...")
            if 'loc' not in data_manager.metrics_df.columns:
                return jsonify({'error': 'LOC data not found in metrics'}), 404
            
            loc_data = data_manager.metrics_df['loc'].dropna().tolist()
            print(f"📍 LOC data points: {len(loc_data)}")
            
            if not loc_data:
                return jsonify({'error': 'No LOC data available'}), 404
                
            # Create simple chart data without Plotly to avoid binary encoding
            chart_data = {
                'data': [{
                    'x': loc_data,
                    'type': 'histogram',
                    'name': 'LOC Distribution',
                    'marker': {'color': '#3498db'}
                }],
                'layout': {
                    'title': 'Lines of Code Distribution',
                    'xaxis': {'title': 'Lines of Code'},
                    'yaxis': {'title': 'Frequency'}
                }
            }
            
        elif chart_type == 'complexity_vs_maintainability':
            print("📍 Processing complexity vs maintainability...")
            required_cols = ['cyclomatic_complexity', 'maintainability_index']
            missing_cols = [col for col in required_cols if col not in data_manager.metrics_df.columns]
            
            if missing_cols:
                return jsonify({'error': f'Missing columns: {missing_cols}'}), 404
            
            complexity_data = data_manager.metrics_df['cyclomatic_complexity'].dropna().tolist()
            maintainability_data = data_manager.metrics_df['maintainability_index'].dropna().tolist()
            problem_ids = data_manager.metrics_df['problem_id'].tolist()
            
            print(f"📍 Complexity data points: {len(complexity_data)}")
            print(f"📍 Maintainability data points: {len(maintainability_data)}")
            
            if not complexity_data or not maintainability_data:
                return jsonify({'error': 'No complexity/maintainability data available'}), 404
                
            # Create simple scatter plot data
            chart_data = {
                'data': [{
                    'x': complexity_data,
                    'y': maintainability_data,
                    'type': 'scatter',
                    'mode': 'markers',
                    'name': 'Problems',
                    'text': problem_ids,
                    'marker': {
                        'color': '#e74c3c',
                        'size': 8
                    }
                }],
                'layout': {
                    'title': 'Complexity vs Maintainability',
                    'xaxis': {'title': 'Cyclomatic Complexity'},
                    'yaxis': {'title': 'Maintainability Index'}
                }
            }
            
        elif chart_type == 'cognitive_complexity':
            print("📍 Processing cognitive complexity...")
            if 'cognitive_complexity' not in data_manager.metrics_df.columns:
                return jsonify({'error': 'Cognitive complexity data not found'}), 404
            
            cog_data = data_manager.metrics_df['cognitive_complexity'].dropna().tolist()
            print(f"📍 Cognitive complexity data points: {len(cog_data)}")
            
            if not cog_data:
                return jsonify({'error': 'No cognitive complexity data available'}), 404
                
            # Create simple box plot data
            chart_data = {
                'data': [{
                    'y': cog_data,
                    'type': 'box',
                    'name': 'Cognitive Complexity',
                    'marker': {'color': '#9b59b6'}
                }],
                'layout': {
                    'title': 'Cognitive Complexity Distribution',
                    'yaxis': {'title': 'Cognitive Complexity'}
                }
            }
            
        else:
            return jsonify({'error': 'Invalid chart type'}), 400
        
        print(f"✅ Successfully created {chart_type} chart")
        return jsonify(chart_data)
    
    except Exception as e:
        print(f"❌ Error creating chart {chart_type}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Chart creation failed: {str(e)}'}), 500
    
        
@app.route('/api/search')
def api_search():
    """Search problems by function name or ID."""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    problems = data_manager.get_all_problems()
    results = [p for p in problems if query in p['function_name'].lower() or query in p['problem_id'].lower()]
    
    return jsonify(results)

@app.route('/debug')
def debug():
    """Debug endpoint to check data loading."""
    problems = data_manager.get_all_problems()
    return jsonify({
        'metrics_loaded': data_manager.metrics_df is not None,
        'samples_loaded': data_manager.samples_data is not None,
        'total_problems': len(problems) if problems else 0,
        'first_problem': problems[0] if problems else None,
        'data_directory': str(data_manager.base_dir),
        'sample_problem_ids': [p['problem_id'] for p in problems[:3]] if problems else []
    })


@app.route('/comparison/<int:problem_number>')
def comparison(problem_number):
    """Show side-by-side comparison of canonical and AI solutions"""
    try:
        # Get canonical solution
        problem_id = f"HumanEval/{problem_number}"
        canonical_data = data_manager.get_problem_details(problem_id)
        if not canonical_data:
            return f"Problem {problem_id} not found", 404
        
        # Get AI solutions for this problem
        if data_manager.evaluation_results is not None:
            ai_solutions = data_manager.evaluation_results[
                data_manager.evaluation_results['task_id'] == problem_id
            ].to_dict('records')
        else:
            ai_solutions = []
        
        # Extract function name from prompt
        prompt = canonical_data.get('prompt', '')
        function_name = "Unknown"
        if 'def ' in prompt:
            function_name = prompt.split('def ')[1].split('(')[0].strip()
        
        return render_template('comparison.html',
                            problem_id=problem_id,
                            function_name=function_name,
                            prompt_preview=prompt[:100] + '...' if len(prompt) > 100 else prompt,
                            canonical_solution=canonical_data.get('canonical_solution', ''),
                            ai_solutions=ai_solutions,
                            test_cases=canonical_data.get('test', ''))
        
    except Exception as e:
        logger.error(f"Error loading comparison for {problem_id}: {e}")
        return f"Error loading comparison: {e}", 500

if __name__ == '__main__':
    if data_manager.load_data():
        print("🚀 Starting Code Quality Dashboard...")
        print("📊 Open http://localhost:5000 in your browser")
        print("🔧 Debug info: http://localhost:5000/debug")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to load data. Please run baseline_analysis.py first.")




