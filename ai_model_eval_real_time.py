#!/usr/bin/env python3
"""
AI_ModelEval with real-time callbacks for web interface
"""

import os
import sys
import pandas as pd
import logging
import traceback
from pathlib import Path
import time
from datetime import datetime
import json

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_layer.config_manager import ConfigManager
from data_layer.dataset_loader import HumanEvalLoader
from model_layer.model_integration import ModelManager
from model_layer.prompt_engine import PromptEngine
from model_layer.code_generator import CodeGenerator
from evaluation_layer.sandbox_executor import SandboxExecutor
from evaluation_layer.metrics_calculator import MetricsCalculator

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealTimeAIModelEval:
    def __init__(self, config_path: str = "config/settings.yaml", progress_callback=None):
        self.config = ConfigManager(config_path)
        self.config.ensure_dirs()
        self.progress_callback = progress_callback or self._default_callback
        
        # Initialize components
        self.model_manager = ModelManager(self.config)
        self.prompt_engine = PromptEngine()
        self.code_generator = CodeGenerator(self.model_manager, self.prompt_engine)
        self.sandbox = SandboxExecutor(timeout=self.config.get("evaluation.timeout_seconds", 30))
        self.metrics_calc = MetricsCalculator()
        
        # State for real-time updates
        self.solutions_generated = 0
        self.tests_executed = 0
        self.tests_passed = 0
    
    def _default_callback(self, step, message, data=None):
        """Default callback that just logs to console"""
        logger.info(f"[{step}] {message}")
        if data:
            logger.debug(f"Data: {data}")
    
    def debug_data_loading(self):
        """Load dataset with progress updates"""
        self.progress_callback("loading_data", "Loading HumanEval dataset...")
        
        loader = HumanEvalLoader(
            self.config.get("paths.repo_url"),
            self.config.get("paths.data_dir")
        )
        
        loader.fetch_repo()
        problems = loader.load_dataset()
        
        self.progress_callback("loading_data", f"Loaded {len(problems)} problems", {
            "problems_loaded": len(problems),
            "sample_problems": [p['task_id'] for p in problems[:3]]
        })
        
        return problems
    
    def debug_model_detection(self, models: list):
        """Check model availability with updates"""
        self.progress_callback("checking_models", "Checking model availability...")
        
        available_models = self.model_manager.get_available_models()
        
        if not available_models:
            self.progress_callback("checking_models", "No models detected, using fallback", {
                "available_models": [],
                "using_fallback": True
            })
            return ["codellama:7b"]
        
        models_to_use = [m for m in models if m in available_models]
        
        self.progress_callback("checking_models", f"Found {len(models_to_use)} available models", {
            "available_models": available_models,
            "selected_models": models_to_use
        })
        
        return models_to_use
    
    def debug_code_generation(self, problems: list, models_to_use: list, num_samples: int):
        """Generate code with incremental updates"""
        self.progress_callback("generating_code", "Starting code generation...")
        
        # Use subset for testing
        test_problems = problems[:3] if len(problems) > 3 else problems
        
        total_tasks = len(test_problems) * len(models_to_use) * num_samples
        completed = 0
        
        all_solutions = []
        
        for problem in test_problems:
            for model in models_to_use:
                for sample_idx in range(num_samples):
                    try:
                        prompt = self.prompt_engine.format_prompt(problem, "zero_shot")
                        generated_code = self.model_manager.generate_code(prompt, model)
                        
                        solution = {
                            'task_id': problem['task_id'],
                            'model': model,
                            'strategy': 'zero_shot',
                            'sample_id': sample_idx,
                            'generated_code': generated_code,
                            'tests': problem.get('test', ''),
                            'prompt': prompt[:100] + '...' if len(prompt) > 100 else prompt
                        }
                        all_solutions.append(solution)
                        
                        completed += 1
                        self.solutions_generated = completed
                        
                        # Update progress
                        progress_pct = (completed / total_tasks) * 100 if total_tasks > 0 else 0
                        self.progress_callback("generating_code", 
                            f"Generated solution {completed}/{total_tasks}",
                            {
                                "progress": progress_pct,
                                "solutions_generated": completed,
                                "current_model": model,
                                "current_problem": problem['task_id']
                            }
                        )
                        
                        # Small delay to avoid rate limits
                        time.sleep(0.5)
                        
                    except Exception as e:
                        logger.error(f"Generation failed: {e}")
                        self.progress_callback("error", f"Generation error: {str(e)}")
        
        df = pd.DataFrame(all_solutions)
        self.progress_callback("generating_code", f"Completed code generation: {len(df)} solutions", {
            "total_solutions": len(df),
            "successful": len(df),
            "failed": 0
        })
        
        return df
    
    def debug_test_execution(self, solutions_df: pd.DataFrame):
        """Execute tests with real-time updates"""
        self.progress_callback("executing_tests", "Starting test execution...")
        
        execution_results = []
        total_tests = len(solutions_df)
        
        for idx, solution in solutions_df.iterrows():
            try:
                if solution.get('error'):
                    self.progress_callback("executing_tests", 
                        f"Skipping solution with generation error: {solution['task_id']}",
                        {"skipped": True}
                    )
                    continue
                
                # Execute test
                result = self.sandbox.execute_safely(
                    solution['generated_code'],
                    solution['tests'],
                    solution['task_id']
                )
                
                execution_results.append({
                    'task_id': solution['task_id'],
                    'model': solution['model'],
                    'strategy': solution['strategy'],
                    'sample_id': solution['sample_id'],
                    'source': result.get('source', 'unknown'),
                    **result
                })
                
                # Update counters
                self.tests_executed += 1
                if result.get('passed'):
                    self.tests_passed += 1
                
                # Update progress
                progress_pct = (idx + 1) / total_tests * 100 if total_tests > 0 else 0
                success_rate = (self.tests_passed / self.tests_executed * 100) if self.tests_executed > 0 else 0
                
                self.progress_callback("executing_tests",
                    f"Test {idx + 1}/{total_tests}: {result['result']}",
                    {
                        "progress": progress_pct,
                        "tests_executed": self.tests_executed,
                        "tests_passed": self.tests_passed,
                        "success_rate": success_rate,
                        "current_result": result['result']
                    }
                )
                
            except Exception as e:
                logger.error(f"Execution failed: {e}")
                execution_results.append({
                    'task_id': solution['task_id'],
                    'model': solution['model'],
                    'strategy': solution['strategy'],
                    'sample_id': solution['sample_id'],
                    'passed': False,
                    'result': f'execution_error: {str(e)}',
                    'output': traceback.format_exc(),
                    'source': 'error'
                })
        
        self.progress_callback("executing_tests", f"Completed test execution: {self.tests_executed} tests", {
            "total_executed": self.tests_executed,
            "passed": self.tests_passed,
            "failed": self.tests_executed - self.tests_passed,
            "success_rate": (self.tests_passed / self.tests_executed * 100) if self.tests_executed > 0 else 0
        })
        
        return execution_results
    
    def run_evaluation(self, models=None, num_samples=None):
        """Run complete evaluation with progress updates"""
        try:
            # Step 1: Load data
            problems = self.debug_data_loading()
            if not problems:
                raise ValueError("No problems loaded")
            
            # Step 2: Check models
            models_to_use = self.debug_model_detection(models or ["codellama:7b"])
            if not models_to_use:
                raise ValueError("No models available")
            
            # Step 3: Generate code
            solutions_df = self.debug_code_generation(problems, models_to_use, num_samples or 2)
            if solutions_df.empty:
                raise ValueError("No solutions generated")
            
            # Step 4: Execute tests
            execution_results = self.debug_test_execution(solutions_df)
            
            # Step 5: Calculate metrics
            self.progress_callback("calculating_metrics", "Calculating evaluation metrics...")
            
            # Combine results
            results_df = solutions_df.merge(
                pd.DataFrame(execution_results),
                on=['task_id', 'model', 'strategy', 'sample_id']
            )
            
            # Calculate metrics
            functional_metrics = self.metrics_calc.calculate_pass_at_k(results_df)
            comparison_report = self.metrics_calc.generate_comparison_report(results_df)
            
            # Save results
            results_dir = Path(self.config.get("paths.results_dir"))
            results_path = results_dir / "evaluation_results.csv"
            results_df.to_csv(results_path, index=False)
            
            report_path = results_dir / "model_comparison.csv"
            comparison_report.to_csv(report_path, index=False)
            
            # Final callback
            stats = {
                "total_solutions": len(results_df),
                "passed_solutions": results_df['passed'].sum(),
                "pass_rate": (results_df['passed'].sum() / len(results_df) * 100) if len(results_df) > 0 else 0,
                "functional_metrics": functional_metrics,
                "models_evaluated": len(models_to_use)
            }
            
            self.progress_callback("complete", "Evaluation completed successfully!", stats)
            
            return results_df, comparison_report
            
        except Exception as e:
            self.progress_callback("error", f"Evaluation failed: {str(e)}")
            raise
        
    def generate_code_with_streaming(self, prompt: str, model: str, task_id: str):
        """Generate code with streaming feedback"""
        try:
            import ollama
            import time
            
            # Start streaming
            stream = ollama.generate(
                model=model,
                prompt=prompt,
                stream=True,
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'max_tokens': 512
                }
            )
            
            generated_code = ""
            for chunk in stream:
                if 'response' in chunk:
                    new_code = chunk['response']
                    generated_code += new_code
                    
                    # Yield each line as it's generated
                    lines = new_code.split('\n')
                    for line in lines:
                        if line.strip():  # Only yield non-empty lines
                            yield {
                                'type': 'code_chunk',
                                'data': {
                                    'line': line,
                                    'task_id': task_id,
                                    'model': model,
                                    'progress': len(generated_code) / 512  # Estimate
                                }
                            }
                            time.sleep(0.05)  # Small delay for visual effect
            
            return generated_code
            
        except Exception as e:
            logger.error(f"Streaming generation failed: {e}")
            return f"# Generation error: {str(e)}"
    
# Standalone execution for testing
if __name__ == "__main__":
    def print_callback(step, message, data=None):
        print(f"[{step.upper()}] {message}")
        if data and 'progress' in data:
            print(f"   Progress: {data['progress']:.1f}%")
    
    evaluator = RealTimeAIModelEval(progress_callback=print_callback)
    results, comparison = evaluator.run_evaluation(
        models=["codellama:7b"],
        num_samples=2
    )
    
    print("\n✅ Evaluation complete!")
    print(f"   Total solutions: {len(results)}")
    print(f"   Passed: {results['passed'].sum()}")