#!/usr/bin/env python3
"""
AI_ModelEval - Main execution script for evaluating AI code generation models
Enhanced with layer-by-layer debugging and individual solution files
ASCII-only logging for Windows compatibility
"""

import os
import sys
import pandas as pd
import logging
import traceback
from pathlib import Path
import time
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_layer.config_manager import ConfigManager
from data_layer.dataset_loader import HumanEvalLoader
from analysis_layer.static_analysis import analyze_dataset
from model_layer.model_integration import ModelManager
from model_layer.prompt_engine import PromptEngine
from model_layer.code_generator import CodeGenerator
from evaluation_layer.sandbox_executor import SandboxExecutor
from evaluation_layer.metrics_calculator import MetricsCalculator

# Setup ASCII-only logging for Windows compatibility
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s',
    handlers=[
        logging.FileHandler(f"evaluation_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DebugTimer:
    """Utility class for timing and debugging each layer"""
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = time.time()
        logger.info(f"STARTING: {operation_name}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time
        if exc_type:
            logger.error(f"FAILED: {self.operation_name} after {elapsed:.2f}s - {exc_val}")
            logger.debug(f"Stack trace: {traceback.format_exc()}")
        else:
            logger.info(f"COMPLETED: {self.operation_name} in {elapsed:.2f}s")

class AIModelEval:
    def __init__(self, config_path: str = "config/settings.yaml"):
        with DebugTimer("Configuration Initialization"):
            self.config = ConfigManager(config_path)
            self.config.ensure_dirs()
            
            # Initialize components with debugging
            logger.info("Initializing system components...")
            self.model_manager = ModelManager(self.config)
            self.prompt_engine = PromptEngine()
            self.code_generator = CodeGenerator(self.model_manager, self.prompt_engine)
            self.sandbox = SandboxExecutor(timeout=self.config.get("evaluation.timeout_seconds", 30))
            self.metrics_calc = MetricsCalculator()
            logger.info("All components initialized successfully")
    
    def save_individual_solution_files(self, solutions_df: pd.DataFrame, base_dir: Path):
        """Save each solution as a separate Python file with organized directory structure"""
        with DebugTimer("Saving Individual Solution Files"):
            solutions_dir = base_dir / "individual_solutions"
            solutions_dir.mkdir(exist_ok=True)
        
            logger.info(f"Creating directory structure in: {solutions_dir}")
            files_created = 0
            errors = 0
        
            for idx, solution in solutions_df.iterrows():
                try:
                    if solution.get('error'):
                        logger.warning(f"Skipping solution with generation error: {solution['task_id']}")
                        continue
                
                # Create directory structure
                    model_clean = solution['model'].replace(':', '_').replace('/', '_')
                    strategy_clean = solution['strategy'].replace(':', '_').replace('/', '_')
                    task_clean = solution['task_id'].replace('/', '_')
                
                    model_dir = solutions_dir / model_clean
                    strategy_dir = model_dir / strategy_clean
                    task_dir = strategy_dir / task_clean
                    task_dir.mkdir(parents=True, exist_ok=True)
                
                # Clean the generated code - remove [PYTHON] tags and extract actual code
                    generated_code = solution['generated_code']
                
                # Remove [PYTHON] tags if present
                    if '[PYTHON]' in generated_code and '[/PYTHON]' in generated_code:
                        # Extract code between [PYTHON] tags
                        start_idx = generated_code.find('[PYTHON]') + len('[PYTHON]')
                        end_idx = generated_code.find('[/PYTHON]')
                        generated_code = generated_code[start_idx:end_idx].strip()
                    elif '```python' in generated_code and '```' in generated_code:
                        # Extract code between ```python blocks
                        start_idx = generated_code.find('```python') + len('```python')
                        end_idx = generated_code.find('```', start_idx)
                        generated_code = generated_code[start_idx:end_idx].strip()
                    elif '```' in generated_code:
                        # Extract code between ``` blocks
                        start_idx = generated_code.find('```') + len('```')
                        end_idx = generated_code.find('```', start_idx)
                        generated_code = generated_code[start_idx:end_idx].strip()
                
                    # Create solution file
                    filename = task_dir / f"sample_{solution['sample_id']}.py"
                
                    # Write the solution with metadata header
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f'"""\n')
                        f.write(f'AI Generated Solution\n')
                        f.write(f'Task ID: {solution["task_id"]}\n')
                        f.write(f'Model: {solution["model"]}\n')
                        f.write(f'Strategy: {solution["strategy"]}\n')
                        f.write(f'Sample ID: {solution["sample_id"]}\n')
                        f.write(f'Generated: {datetime.now().isoformat()}\n')
                        f.write(f'"""\n\n')
                        f.write(generated_code)
                
                # Create test file for this solution
                    test_filename = task_dir / f"test_sample_{solution['sample_id']}.py"
                    with open(test_filename, 'w', encoding='utf-8') as f:
                        f.write(f'"""\n')
                        f.write(f'Test for AI Generated Solution\n')
                        f.write(f'Task ID: {solution["task_id"]}\n')
                        f.write(f'Model: {solution["model"]}\n')
                        f.write(f'"""\n\n')
                        f.write(generated_code)
                        f.write('\n\n')
                        f.write(solution['tests'])
                
                    files_created += 2
                    if files_created % 10 == 0:
                        logger.debug(f"Created {files_created} files so far...")
                    
                except Exception as e:
                    errors += 1
                    logger.error(f"Failed to save solution file for {solution['task_id']}: {e}")
                    logger.debug(f"Solution data: {solution.get('generated_code', 'NO_CODE')[:100]}...")
        
            logger.info(f"Saved {files_created} individual files ({errors} errors)")
            return solutions_dir    


    def debug_model_detection(self, models: list) -> list:
        """Debug model availability with detailed logging"""
        with DebugTimer("Model Detection and Validation"):
            logger.info("Checking model availability...")
            
            available_models = self.model_manager.get_available_models()
            logger.info(f"Available models: {available_models}")
            
            if not available_models:
                logger.warning("No models detected via API")
                logger.info("Attempting fallback to common models...")
                models_to_use = ["codellama:7b"]
                logger.info(f"Will attempt to use: {models_to_use}")
            else:
                # Use only available models
                models_to_use = [m for m in models if m in available_models]
                if not models_to_use:
                    logger.error("No available models found from requested list!")
                    logger.info(f"Requested: {models}, Available: {available_models}")
                    logger.info("Try pulling a model first: ollama pull codellama:7b")
                    return []
            
            logger.info(f"Final model selection: {models_to_use}")
            return models_to_use
    
    def debug_data_loading(self):
        """Debug data loading process"""
        with DebugTimer("Dataset Loading"):
            logger.info("Loading HumanEval dataset...")
            loader = HumanEvalLoader(
                self.config.get("paths.repo_url"),
                self.config.get("paths.data_dir")
            )
            
            logger.debug("Fetching repository...")
            loader.fetch_repo()
            
            logger.debug("Loading problems from dataset...")
            problems = loader.load_dataset()
            
            logger.info(f"Loaded {len(problems)} problems")
            if problems:
                logger.debug(f"Sample problem IDs: {[p['task_id'] for p in problems[:3]]}")
            
            return problems
    
    def debug_code_generation(self, problems: list, models_to_use: list, num_samples: int):
        """Debug code generation with detailed progress tracking"""
        with DebugTimer("Code Generation"):
            logger.info("Generating code solutions...")
            logger.debug(f"Generating {num_samples} samples each for {len(problems)} problems using {len(models_to_use)} models")
            
            # Use a small subset for testing
            test_problems = problems[:3]  # Reduced from 5 to 3 for faster testing
            
            solutions_df = self.code_generator.generate_solutions(
                test_problems,
                models_to_use,
                num_samples=num_samples,
                strategies=["zero_shot"]
            )
            
            # Analyze generation results
            total_solutions = len(solutions_df)
            if 'error' in solutions_df.columns:
                successful_solutions = len(solutions_df[solutions_df['error'].isna()])
            else:
                successful_solutions = total_solutions
            failed_solutions = total_solutions - successful_solutions
            
            logger.info(f"Generation results: {successful_solutions} successful, {failed_solutions} failed")
            
            if failed_solutions > 0:
                logger.warning(f"{failed_solutions} solutions failed generation")
                if 'error' in solutions_df.columns:
                    failed_samples = solutions_df[solutions_df['error'].notna()]
                    for _, failed in failed_samples.head(3).iterrows():
                        logger.debug(f"Failed sample: {failed['task_id']} - {failed.get('error', 'Unknown error')}")
            
            return solutions_df
    
        """Debug test execution using individual solution files"""
    def debug_test_execution(self, solutions_df: pd.DataFrame):
        with DebugTimer("Test Execution from Individual Files"):
            logger.info("Executing tests from individual solution files...")
            execution_results = []
            total_tests = len(solutions_df)
            
            for idx, solution in solutions_df.iterrows():
                try:
                    logger.debug(f"Testing solution {idx+1}/{total_tests}: {solution['task_id']} - {solution['model']}")
                    
                    if solution.get('error'):
                        logger.warning(f"Skipping execution for solution with generation error")
                        execution_results.append({
                            'task_id': solution['task_id'],
                            'model': solution['model'],
                            'strategy': solution['strategy'],
                            'sample_id': solution['sample_id'],
                            'passed': False,
                            'result': 'generation_error',
                            'output': solution.get('error', 'Unknown error'),
                            'source': 'dataframe'
                        })
                        continue
                    
                    # Get the individual solution file path
                    model_clean = solution['model'].replace(':', '_').replace('/', '_')
                    strategy_clean = solution['strategy'].replace(':', '_').replace('/', '_')
                    task_clean = solution['task_id'].replace('/', '_')
                    
                    solution_file = (Path(self.config.get("paths.results_dir")) / 
                                   "individual_solutions" / model_clean / strategy_clean / 
                                   task_clean / f"sample_{solution['sample_id']}.py")
                    
                    if not solution_file.exists():
                        logger.warning(f"Solution file not found: {solution_file}")
                        execution_results.append({
                            'task_id': solution['task_id'],
                            'model': solution['model'],
                            'strategy': solution['strategy'],
                            'sample_id': solution['sample_id'],
                            'passed': False,
                            'result': 'file_not_found',
                            'output': f'Solution file not found: {solution_file}',
                            'source': 'dataframe'
                        })
                        continue
                    
                    # Read and extract ONLY the function code (skip docstring header)
                    logger.debug(f"Reading solution from: {solution_file}")
                    with open(solution_file, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    
                    # FIX: Extract only the Python function, not the docstring header
                    code_lines = []
                    in_docstring = False
                    docstring_delimiter = None
                    
                    for line in file_content.split('\n'):
                        stripped = line.strip()
                        
                        # Check for start of docstring
                        if (stripped.startswith('"""') or stripped.startswith("'''")) and not in_docstring:
                            in_docstring = True
                            docstring_delimiter = stripped[:3]
                            continue
                        
                        # Check for end of docstring
                        if in_docstring and stripped.endswith(docstring_delimiter):
                            in_docstring = False
                            continue
                        
                        # If we're not in a docstring, keep the line
                        if not in_docstring:
                            code_lines.append(line)
                    
                    # Join the code lines
                    actual_code = '\n'.join(code_lines).strip()
                    
                    # If no code extracted, fall back to dataframe
                    if not actual_code:
                        logger.warning(f"No executable code found in {solution_file}, using dataframe")
                        actual_code = solution['generated_code']
                        source = 'dataframe_fallback'
                    else:
                        source = 'file'
                    
                    logger.debug(f"Extracted code length: {len(actual_code)} chars")
                    
                    # Execute the solution
                    result = self.sandbox.execute_safely(
                        actual_code,
                        solution['tests'],
                        solution['task_id']
                    )
                    
                    execution_results.append({
                        'task_id': solution['task_id'],
                        'model': solution['model'],
                        'strategy': solution['strategy'],
                        'sample_id': solution['sample_id'],
                        'source': source,
                        **result
                    })
                    
                    logger.debug(f"Execution result: {result['result']} (source: {source})")
                    
                except Exception as e:
                    logger.error(f"Execution failed for solution {idx}: {e}")
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
            
            # Log source statistics
            sources = [r.get('source', 'unknown') for r in execution_results]
            source_counts = {source: sources.count(source) for source in set(sources)}
            logger.info(f"Execution sources: {source_counts}")
            
            return execution_results
                
    def run_full_evaluation(self, models: list = None, num_samples: int = None):
        """Run complete evaluation pipeline with enhanced debugging"""
        logger.info("Starting AI Model Evaluation Pipeline with Enhanced Debugging")
        logger.info("=" * 60)
        
        # Configuration
        if models is None:
            models = self.config.get("models.default_models", ["codellama:7b"])
        
        if num_samples is None:
            num_samples = self.config.get("evaluation.num_samples_per_task", 5)
        
        logger.info(f"Configuration: {len(models)} models, {num_samples} samples per task")
        
        try:
            # Step 1: Load dataset with debugging
            problems = self.debug_data_loading()
            if not problems:
                logger.error("No problems loaded from dataset!")
                return None, None
            
            # Step 2: Check available models with debugging
            models_to_use = self.debug_model_detection(models)
            if not models_to_use:
                logger.error("No models available for evaluation!")
                return None, None
            
            # Step 3: Generate solutions with debugging
            solutions_df = self.debug_code_generation(problems, models_to_use, num_samples)
            if solutions_df.empty:
                logger.error("No solutions generated!")
                return None, None
            
            # Save generated solutions to CSV
            solutions_path = Path(self.config.get("paths.results_dir")) / "generated_solutions.csv"
            solutions_df.to_csv(solutions_path, index=False)
            logger.info(f"Saved solutions CSV to: {solutions_path}")
            
            # Save individual solution files
            solutions_dir = self.save_individual_solution_files(solutions_df, Path(self.config.get("paths.results_dir")))
            logger.info(f"Individual solutions saved to: {solutions_dir}")
            
            # Step 4: Execute tests with debugging
            execution_results = self.debug_test_execution(solutions_df)
            
            # Combine results
            with DebugTimer("Results Combination"):
                results_df = solutions_df.merge(
                    pd.DataFrame(execution_results),
                    on=['task_id', 'model', 'strategy', 'sample_id']
                )
                logger.info(f"Combined {len(results_df)} results")
            
            # Step 5: Calculate metrics with debugging
            with DebugTimer("Metrics Calculation"):
                logger.info("Calculating evaluation metrics...")
                functional_metrics = self.metrics_calc.calculate_pass_at_k(results_df)
                comparison_report = self.metrics_calc.generate_comparison_report(results_df)
                logger.info("Metrics calculated successfully")
            
            # Step 6: Save results
            with DebugTimer("Results Persistence"):
                results_path = Path(self.config.get("paths.results_dir")) / "evaluation_results.csv"
                results_df.to_csv(results_path, index=False)
                
                report_path = Path(self.config.get("paths.results_dir")) / "model_comparison.csv"
                comparison_report.to_csv(report_path, index=False)
                
                logger.info(f"Results saved to:")
                logger.info(f"   Solutions: {solutions_path}")
                logger.info(f"   Individual Files: {solutions_dir}")
                logger.info(f"   Full Results: {results_path}")
                logger.info(f"   Comparison: {report_path}")
            
            # Step 7: Print summary
            self.print_detailed_summary(functional_metrics, comparison_report, results_df)
            
            return results_df, comparison_report
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            logger.debug(f"Full stack trace: {traceback.format_exc()}")
            raise
    
    def print_detailed_summary(self, functional_metrics: dict, comparison_report: pd.DataFrame, results_df: pd.DataFrame):
        """Print comprehensive evaluation summary"""
        logger.info("EVALUATION COMPLETE!")
        logger.info("=" * 60)
        
        # Overall statistics
        total_solutions = len(results_df)
        passed_solutions = results_df['passed'].sum()
        pass_rate = (passed_solutions / total_solutions) * 100 if total_solutions > 0 else 0
        
        logger.info("OVERALL STATISTICS:")
        logger.info(f"   Total Solutions: {total_solutions}")
        logger.info(f"   Passed Solutions: {passed_solutions}")
        logger.info(f"   Overall Pass Rate: {pass_rate:.1f}%")
        
        logger.info("FUNCTIONAL CORRECTNESS METRICS:")
        for metric, value in functional_metrics.items():
            logger.info(f"   {metric}: {value:.3f}")
        
        logger.info("\nMODEL COMPARISON:")
        for _, model_row in comparison_report.iterrows():
            logger.info(f"   {model_row['model']}:")
            logger.info(f"     Pass Rate: {model_row['pass_rate']:.3f}")
            logger.info(f"     Pass@1: {model_row['pass@1']:.3f}")
            logger.info(f"     Pass@5: {model_row['pass@5']:.3f}")
            logger.info(f"     Total Tests: {model_row['total_tests']}")

def main():
    """Main execution function with enhanced error handling"""
    try:
        logger.info("AI Model Evaluation Starting...")
        
        evaluator = AIModelEval()
        
        # Run evaluation with minimal configuration for testing
        logger.info("Starting evaluation with test configuration...")
        results, comparison = evaluator.run_full_evaluation(
            models=["codellama:7b"],  # Start with one model
            num_samples=2  # Fewer samples for initial testing
        )
        
        if results is not None:
            logger.info("\nEvaluation completed successfully!")
            logger.info("Start the dashboard with: python dashboard/app.py")
        else:
            logger.error("Evaluation failed to produce results")
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"Critical failure in main execution: {e}")
        logger.error("Check the debug log file for detailed traceback")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()