from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import os
from pathlib import Path
import plotly.express as px
import plotly.utils

app = Flask(__name__)

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
            # Load baseline metrics
            metrics_path = self.base_dir / "results" / "baseline" / "human_baseline_metrics.csv"
            if metrics_path.exists():
                self.metrics_df = pd.read_csv(metrics_path)
                print(f"✅ Loaded baseline metrics for {len(self.metrics_df)} problems")
            
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

if __name__ == '__main__':
    if data_manager.load_data():
        print("🚀 Starting Enhanced AI ModelEval Dashboard...")
        print("📊 Open http://localhost:5000 in your browser")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to load data. Please run evaluation first.")