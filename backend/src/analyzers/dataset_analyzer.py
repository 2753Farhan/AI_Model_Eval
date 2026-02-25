# src/analyzers/dataset_analyzer.py
"""
Dataset Analysis & Visualization Module
Integrates with existing codebase
"""

import json
import gzip
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import webbrowser 
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import logging
from ..executors import SandboxExecutor

logger = logging.getLogger(__name__)


class DatasetAnalyzer:
    """Analyze and visualize dataset performance"""
    
    def __init__(self, sandbox: Optional[SandboxExecutor] = None):
        self.sandbox = sandbox or SandboxExecutor(timeout=30)
        self.results = []
        self.problems = []
        self.stats = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'error_types': Counter(),
            'by_difficulty': {'Easy': {'total': 0, 'passed': 0},
                             'Medium': {'total': 0, 'passed': 0},
                             'Hard': {'total': 0, 'passed': 0}},
            'test_case_stats': {'total': 0, 'passed': 0, 'failed': 0}
        }
        self.start_time = datetime.now()
    
    def load_dataset(self, data_path: str = "data/data/HumanEval.jsonl.gz") -> bool:
        """Load dataset from file"""
        data_file = Path(data_path)
        if not data_file.exists():
            logger.error(f"Data file not found: {data_file}")
            return False
        
        try:
            if str(data_file).endswith('.gz'):
                opener = gzip.open(data_file, 'rt', encoding='utf-8')
            else:
                opener = open(data_file, 'r', encoding='utf-8')
            
            with opener as f:
                for line in f:
                    data = json.loads(line)
                    self.problems.append({
                        'task_id': data.get('task_id'),
                        'prompt': data.get('prompt', ''),
                        'canonical_solution': data.get('canonical_solution', ''),
                        'test': data.get('test', ''),
                        'entry_point': data.get('entry_point'),
                        'complexity': self._estimate_complexity(data.get('canonical_solution', '')),
                        'test_count': len([l for l in data.get('test', '').split('\n') if 'assert' in l])
                    })
            
            logger.info(f"✅ Loaded {len(self.problems)} problems")
            return True
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return False
    
    def _estimate_complexity(self, code: str) -> str:
        """Estimate problem complexity"""
        if not code:
            return 'Unknown'
        
        lines = code.split('\n')
        line_count = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        loops = code.count('for ') + code.count('while ')
        conditionals = code.count('if ') + code.count('else:') + code.count('elif ')
        
        complexity_score = line_count + loops * 2 + conditionals
        
        if complexity_score < 5:
            return 'Easy'
        elif complexity_score < 10:
            return 'Medium'
        else:
            return 'Hard'
    
    async def analyze_all(self, limit: Optional[int] = None):
        """Run analysis on all problems"""
        problems_to_analyze = self.problems[:limit] if limit else self.problems
        
        for i, problem in enumerate(problems_to_analyze, 1):
            print(f"\r  Analyzing: {i}/{len(problems_to_analyze)} - {problem['task_id']}", end='')
            
            result = await self._analyze_problem(problem)
            self.results.append(result)
            
            # Update stats
            self.stats['total'] += 1
            if result['passed']:
                self.stats['passed'] += 1
                self.stats['by_difficulty'][problem['complexity']]['passed'] += 1
            else:
                self.stats['failed'] += 1
                self.stats['error_types'][result['error_type']] += 1
            
            self.stats['by_difficulty'][problem['complexity']]['total'] += 1
            self.stats['test_case_stats']['total'] += result['test_count']
            self.stats['test_case_stats']['passed'] += result['tests_passed']
            self.stats['test_case_stats']['failed'] += result['test_count'] - result['tests_passed']
        
        print("\n✅ Analysis complete!")
    
    async def _analyze_problem(self, problem: Dict) -> Dict:
        """Analyze a single problem"""
        # Prepare code
        code = self._prepare_code(problem)
        test_cases = self._prepare_test_cases(problem)
        
        # Execute
        result = await self.sandbox.execute_safely(
            code=code,
            test_cases=test_cases,
            problem_id=problem['task_id'],
            language="python"
        )
        
        # Categorize error
        error_type = 'None' if result.get('passed') else self._categorize_error(result.get('output', ''))
        
        return {
            'task_id': problem['task_id'],
            'passed': result.get('passed', False),
            'error_type': error_type,
            'time_ms': result.get('execution_time_ms', 0),
            'test_count': len(test_cases),
            'tests_passed': len([t for t in result.get('test_results', []) if t.get('passed')]),
            'complexity': problem['complexity'],
            'output': result.get('output', '')[:200] if not result.get('passed') else ''
        }
    
    def _prepare_code(self, problem: Dict) -> str:
        """Prepare code for execution"""
        entry_point = problem['entry_point']
        prompt = problem['prompt']
        body = problem['canonical_solution']
        
        # Extract signature
        signature = None
        for line in prompt.split('\n'):
            if line.strip().startswith('def ' + entry_point):
                signature = line.rstrip()
                break
        
        if not signature:
            signature = f"def {entry_point}(*args, **kwargs):"
        
        # Add imports
        imports = self._get_imports(body, prompt)
        
        # Combine
        if body and not body[0].isspace():
            indented_body = '\n'.join('    ' + line if line.strip() else line 
                                      for line in body.split('\n'))
        else:
            indented_body = body
        
        return imports + f"\n{signature}\n{indented_body}"
    
    def _get_imports(self, code: str, prompt: str) -> str:
        """Get necessary imports"""
        imports = []
        combined = code + ' ' + prompt
        
        if 'List' in combined or 'Tuple' in combined or 'Optional' in combined or 'Any' in combined:
            imports.append("from typing import List, Tuple, Optional, Any, Dict, Set")
        if 'math.' in combined or 'math' in combined:
            imports.append("import math")
        if 'copy.' in combined or 'copy' in combined:
            imports.append("import copy")
        if 'defaultdict' in combined:
            imports.append("from collections import defaultdict")
        if 'Counter' in combined:
            imports.append("from collections import Counter")
        
        return '\n'.join(imports) + '\n\n' if imports else ''
    
    def _prepare_test_cases(self, problem: Dict) -> List[Dict]:
        """Prepare test cases"""
        test_cases = []
        entry_point = problem['entry_point']
        
        for line in problem['test'].split('\n'):
            line = line.strip()
            if line.startswith('assert'):
                assertion = line.replace('candidate', entry_point)
                test_cases.append({'assertion': assertion})
        
        return test_cases
    
    def _categorize_error(self, output: str) -> str:
        """Categorize error type"""
        if 'SyntaxError' in output:
            return 'SyntaxError'
        elif 'NameError' in output:
            return 'NameError'
        elif 'TypeError' in output:
            return 'TypeError'
        elif 'ValueError' in output:
            return 'ValueError'
        elif 'IndexError' in output:
            return 'IndexError'
        elif 'KeyError' in output:
            return 'KeyError'
        elif 'AttributeError' in output:
            return 'AttributeError'
        elif 'ImportError' in output:
            return 'ImportError'
        elif 'Timeout' in output or 'timed out' in output:
            return 'Timeout'
        elif 'AssertionError' in output:
            return 'AssertionError'
        else:
            return 'Other'
    
    def generate_report(self, output_dir: str = "analysis_reports"):
        """Generate comprehensive analysis report"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Generate HTML Report
        self._generate_html_report(output_path / f"report_{timestamp}.html")
        
        # 2. Generate CSV Data
        self._generate_csv_data(output_path / f"data_{timestamp}.csv")
        
        # 3. Generate Visualizations
        self._generate_visualizations(output_path, timestamp)
        
        print(f"\n✅ Reports saved to {output_path}/")
        
        # Open HTML report in browser
        html_path = output_path / f"report_{timestamp}.html"
        webbrowser.open(f"file://{html_path.absolute()}")
    
    def _generate_html_report(self, filepath: Path):
        """Generate interactive HTML report"""
        pass_rate = (self.stats['passed'] / self.stats['total'] * 100) if self.stats['total'] else 0
        
        # Create summary tables
        passed_df = pd.DataFrame([r for r in self.results if r['passed']])
        failed_df = pd.DataFrame([r for r in self.results if not r['passed']])
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dataset Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; }}
                .summary {{ background: #f8f9fa; padding: 20px; border-radius: 5px; }}
                .stat {{ font-size: 24px; font-weight: bold; color: #3498db; }}
                .passed {{ color: #27ae60; }}
                .failed {{ color: #e74c3c; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>📊 Dataset Analysis Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <div class="summary">
                <h2>Summary Statistics</h2>
                <p><span class="stat">{self.stats['total']}</span> Total Problems</p>
                <p><span class="stat passed">{self.stats['passed']}</span> Passed ({pass_rate:.1f}%)</p>
                <p><span class="stat failed">{self.stats['failed']}</span> Failed</p>
                <p>Total Test Cases: {self.stats['test_case_stats']['total']}</p>
                <p>Test Cases Passed: {self.stats['test_case_stats']['passed']} 
                   ({self.stats['test_case_stats']['passed']/self.stats['test_case_stats']['total']*100:.1f}%)</p>
            </div>
            
            <h2>Error Breakdown</h2>
            <table>
                <tr>
                    <th>Error Type</th>
                    <th>Count</th>
                </tr>
        """
        
        for error_type, count in self.stats['error_types'].most_common():
            html += f"""
                <tr>
                    <td>{error_type}</td>
                    <td>{count}</td>
                </tr>
            """
        
        html += """
            </table>
            
            <h2>Complexity Analysis</h2>
            <table>
                <tr>
                    <th>Difficulty</th>
                    <th>Total</th>
                    <th>Passed</th>
                    <th>Pass Rate</th>
                </tr>
        """
        
        for diff, stats in self.stats['by_difficulty'].items():
            if stats['total'] > 0:
                rate = stats['passed'] / stats['total'] * 100
                html += f"""
                <tr>
                    <td>{diff}</td>
                    <td>{stats['total']}</td>
                    <td>{stats['passed']}</td>
                    <td>{rate:.1f}%</td>
                </tr>
                """
        
        html += """
            </table>
            
            <h2>Failed Problems Details</h2>
            <table>
                <tr>
                    <th>Task ID</th>
                    <th>Error Type</th>
                    <th>Tests Passed</th>
                    <th>Error Message</th>
                </tr>
        """
        
        for result in self.results:
            if not result['passed']:
                html += f"""
                <tr>
                    <td>{result['task_id']}</td>
                    <td>{result['error_type']}</td>
                    <td>{result['tests_passed']}/{result['test_count']}</td>
                    <td>{result['output'][:100]}</td>
                </tr>
                """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def _generate_csv_data(self, filepath: Path):
        """Generate CSV data"""
        df = pd.DataFrame(self.results)
        df.to_csv(filepath, index=False)
    
    def _generate_visualizations(self, output_dir: Path, timestamp: str):
        """Generate visualization images"""
        # 1. Pass/Fail Pie Chart
        plt.figure(figsize=(8, 8))
        plt.pie([self.stats['passed'], self.stats['failed']], 
                labels=['Passed', 'Failed'],
                autopct='%1.1f%%',
                colors=['#27ae60', '#e74c3c'])
        plt.title('Overall Pass Rate')
        plt.savefig(output_dir / f'pie_{timestamp}.png')
        plt.close()
        
        # 2. Error Types Bar Chart
        if self.stats['error_types']:
            plt.figure(figsize=(12, 6))
            errors = dict(self.stats['error_types'].most_common(10))
            plt.bar(errors.keys(), errors.values(), color='#3498db')
            plt.title('Top 10 Error Types')
            plt.xlabel('Error Type')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(output_dir / f'errors_{timestamp}.png')
            plt.close()
        
        # 3. Complexity Analysis
        difficulties = []
        pass_rates = []
        for diff, stats in self.stats['by_difficulty'].items():
            if stats['total'] > 0:
                difficulties.append(diff)
                pass_rates.append(stats['passed'] / stats['total'] * 100)
        
        plt.figure(figsize=(10, 6))
        plt.bar(difficulties, pass_rates, color=['#2ecc71', '#f39c12', '#e74c3c'])
        plt.title('Pass Rate by Difficulty')
        plt.xlabel('Difficulty')
        plt.ylabel('Pass Rate (%)')
        plt.ylim(0, 100)
        for i, v in enumerate(pass_rates):
            plt.text(i, v + 1, f'{v:.1f}%', ha='center')
        plt.savefig(output_dir / f'complexity_{timestamp}.png')
        plt.close()
    
    def print_summary(self):
        """Print summary to console"""
        elapsed = datetime.now() - self.start_time
        pass_rate = (self.stats['passed'] / self.stats['total'] * 100) if self.stats['total'] else 0
        test_pass_rate = (self.stats['test_case_stats']['passed'] / self.stats['test_case_stats']['total'] * 100) if self.stats['test_case_stats']['total'] else 0
        
        print("\n" + "=" * 60)
        print("DATASET ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"⏱️  Time: {elapsed.total_seconds():.1f}s")
        print(f"📊 Total Problems: {self.stats['total']}")
        print(f"✅ Passed: {self.stats['passed']} ({pass_rate:.1f}%)")
        print(f"❌ Failed: {self.stats['failed']}")
        print(f"📋 Total Test Cases: {self.stats['test_case_stats']['total']}")
        print(f"📋 Tests Passed: {self.stats['test_case_stats']['passed']} ({test_pass_rate:.1f}%)")
        
        if self.stats['error_types']:
            print("\n🔍 Top Error Types:")
            for error, count in self.stats['error_types'].most_common(5):
                print(f"  • {error}: {count}")
        
        print("\n📈 By Difficulty:")
        for diff, stats in self.stats['by_difficulty'].items():
            if stats['total'] > 0:
                rate = stats['passed'] / stats['total'] * 100
                print(f"  • {diff}: {stats['passed']}/{stats['total']} ({rate:.1f}%)")
    
    def get_failing_tests(self) -> List[Dict]:
        """Get list of failing tests with details"""
        return [r for r in self.results if not r['passed']]
    
    def get_slow_tests(self, threshold_ms: float = 1000) -> List[Dict]:
        """Get tests that run slow"""
        return [r for r in self.results if r['time_ms'] > threshold_ms]
    
    def cleanup(self):
        """Clean up resources"""
        self.sandbox.cleanup()