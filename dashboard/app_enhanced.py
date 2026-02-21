from flask import Flask, render_template, request, jsonify
import pandas as pd

from pathlib import Path
import plotly.express as px
from datetime import datetime
import logging


app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedDashboardDataManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.metrics_df = None
        self.samples_data = None
        self.evaluation_results = None
        self.model_comparison = None
        self.load_data()
    
    def load_data(self):
        """Load all data for enhanced dashboard"""
        try:
            # Load evaluation results
            results_path = self.base_dir / "results" / "evaluation_results.csv"
            if results_path.exists():
                self.evaluation_results = pd.read_csv(results_path)
                print(f"✅ Loaded evaluation results for {len(self.evaluation_results)} samples")
            
            # Load model comparison
            comparison_path = self.base_dir / "results" / "model_comparison.csv"
            if comparison_path.exists():
                self.model_comparison = pd.read_csv(comparison_path)
                print(f"✅ Loaded comparison for {len(self.model_comparison)} models")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def get_model_comparison_data(self):
        """Get data for model comparison"""
        if self.model_comparison is None:
            return []
        
        return self.model_comparison.to_dict('records')
    
    def get_evaluation_results(self, model_filter=None):
        """Get evaluation results with optional model filter"""
        if self.evaluation_results is None:
            return []
        
        results = self.evaluation_results
        if model_filter:
            results = results[results['model'] == model_filter]
        
        return results.to_dict('records')
    
    def get_single_result(self, task_id, model, sample_id):
        """Get a single result by task_id, model, and sample_id"""
        if self.evaluation_results is None:
            return None
        
        result = self.evaluation_results[
            (self.evaluation_results['task_id'] == task_id) &
            (self.evaluation_results['model'] == model) &
            (self.evaluation_results['sample_id'] == sample_id)
        ]
        
        if not result.empty:
            return result.iloc[0].to_dict()
        return None
# Initialize enhanced data manager
data_manager = EnhancedDashboardDataManager()

@app.route('/')
def index():
    """Enhanced main dashboard"""
    model_comparison = data_manager.get_model_comparison_data()
    
    return render_template('enhanced_index.html', 
                         model_comparison=model_comparison,
                         has_evaluation_data=len(model_comparison) > 0)

@app.route('/model_comparison')
def model_comparison():
    """Model comparison page"""
    models = data_manager.get_model_comparison_data()
    return render_template('model_comparison.html', models=models)

@app.route('/evaluation_results')
def evaluation_results():
    """Detailed evaluation results"""
    model_filter = request.args.get('model')
    results = data_manager.get_evaluation_results(model_filter)
    return render_template('evaluation_results.html', 
                         results=results, 
                         model_filter=model_filter)

@app.route('/api/model_metrics')
def api_model_metrics():
    """API for model metrics charts"""
    models = data_manager.get_model_comparison_data()
    
    if not models:
        return jsonify({'error': 'No model comparison data available'})
    
    # Create comparison chart data
    model_names = [m['model'] for m in models]
    pass_rates = [m['pass_rate'] for m in models]
    pass_at_1 = [m.get('pass@1', 0) for m in models]
    
    chart_data = {
        'pass_rates': {
            'x': model_names,
            'y': pass_rates,
            'type': 'bar',
            'name': 'Pass Rate'
        },
        'pass_at_1': {
            'x': model_names,
            'y': pass_at_1,
            'type': 'bar',
            'name': 'Pass@1'
        }
    }
    
    return jsonify(chart_data)

# @app.route('/result/<task_id>/<model>/<int:sample_id>')
# def result_details(task_id, model, sample_id):
#     """Result details page"""
#     try:
#         # Restore slashes from safe separator
#         task_id = task_id.replace('---', '/')
#         model = model.replace('---', '/')
        
#         logger.info(f"Loading result details for: {task_id}, {model}, {sample_id}")
        
#         # Load results data
#         results_path = Path(__file__).parent.parent / "results" / "evaluation_results.csv"
#         if results_path.exists():
#             results_df = pd.read_csv(results_path)
            
#             # Find the specific result
#             result_row = results_df[
#                 (results_df['task_id'] == task_id) &
#                 (results_df['model'] == model) &
#                 (results_df['sample_id'] == sample_id)
#             ]
            
#             if not result_row.empty:
#                 result = result_row.iloc[0].to_dict()
#                 logger.info(f"Found result: {result.get('result', 'N/A')}")
                
#                 return render_template('result_details.html', 
#                                      result=result,
#                                      task_id=task_id,
#                                      model=model,
#                                      sample_id=sample_id)
#             else:
#                 # Debug: Show what's actually in the dataframe
#                 logger.error(f"Result not found: {task_id} - {model} - {sample_id}")
#                 logger.error(f"Available task IDs: {results_df['task_id'].unique()[:5]}")
#                 logger.error(f"Available models: {results_df['model'].unique()[:5]}")
#                 logger.error(f"Matching rows: {results_df[results_df['task_id'] == task_id].shape[0]}")
#                 logger.error(f"Matching models: {results_df[results_df['model'] == model].shape[0]}")
                
#                 return f"Result not found: {task_id} - {model} - {sample_id}<br>" \
#                        f"Available task IDs: {list(results_df['task_id'].unique()[:5])}<br>" \
#                        f"Available models: {list(results_df['model'].unique()[:5])}", 404
#         else:
#             logger.error(f"Results file not found at: {results_path}")
#             return "Results file not found", 404
            
#     except Exception as e:
#         logger.error(f"Error loading result details: {e}")
#         import traceback
#         traceback.print_exc()
#         return f"Error: {str(e)}", 500
    
    
@app.route('/result')
def result_details():
    """Result details page with individual test results"""
    try:
        task_id = request.args.get('task_id')
        model = request.args.get('model')
        sample_id = request.args.get('sample_id', type=int)
        
        if not all([task_id, model, sample_id is not None]):
            return "Missing parameters", 400
        
        logger.info(f"Loading result details for: {task_id}, {model}, {sample_id}")
        
        # Load results data
        results_path = Path(__file__).parent.parent / "results" / "evaluation_results.csv"
        if results_path.exists():
            results_df = pd.read_csv(results_path)
            
            # Find the specific result
            result_row = results_df[
                (results_df['task_id'] == task_id) &
                (results_df['model'] == model) &
                (results_df['sample_id'] == sample_id)
            ]
            
            if not result_row.empty:
                result = result_row.iloc[0].to_dict()
                logger.info(f"Found result: {result.get('result', 'N/A')}")
                
                # Parse test_results if it's stored as a JSON string
                if 'test_results' in result and isinstance(result['test_results'], str):
                    try:
                        result['test_results'] = json.loads(result['test_results'])
                    except (json.JSONDecodeError, TypeError):
                        result['test_results'] = []
                
                # Ensure numeric fields are properly typed
                if 'total_tests' in result:
                    try:
                        result['total_tests'] = int(result['total_tests'])
                    except (ValueError, TypeError):
                        result['total_tests'] = 0
                
                if 'passed_tests' in result:
                    try:
                        result['passed_tests'] = int(result['passed_tests'])
                    except (ValueError, TypeError):
                        result['passed_tests'] = 0
                
                if 'failed_tests' in result:
                    try:
                        result['failed_tests'] = int(result['failed_tests'])
                    except (ValueError, TypeError):
                        result['failed_tests'] = 0
                
                return render_template('result_details.html', 
                                     result=result,
                                     task_id=task_id,
                                     model=model,
                                     sample_id=sample_id)
            else:
                logger.error(f"Result not found: {task_id} - {model} - {sample_id}")
                return f"""
                <h2>Result Not Found</h2>
                <p>Task: {task_id}</p>
                <p>Model: {model}</p>
                <p>Sample: {sample_id}</p>
                <hr>
                <a href="/evaluation_results" class="btn btn-primary">Back to Results</a>
                """, 404
        else:
            return f"Results file not found", 404
            
    except Exception as e:
        logger.error(f"Error loading result details: {e}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}", 500
        
if __name__ == '__main__':
    if data_manager.load_data():
        print("🚀 Starting Enhanced AI ModelEval Dashboard...")
        print("📊 Open http://localhost:5001 in your browser")
        app.run(debug=True, host='0.0.0.0', port=5001)
    else:
        print("❌ Failed to load data. Please run evaluation first.")