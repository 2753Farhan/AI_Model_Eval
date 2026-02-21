#!/usr/bin/env python3
"""
AI_ModelEval - Main execution script for evaluating AI code generation models
Enhanced with layer-by-layer debugging and individual solution files
ASCII-only logging for Windows compatibility
With automatic model fallback based on available space
"""

import os
import sys
import pandas as pd
import logging
import traceback
from pathlib import Path
import time
from datetime import datetime
import shutil
import psutil

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


class DiskSpaceManager:
    """Manages disk space and selects appropriate models based on available space"""
    
    # Model hierarchy from largest to smallest (approximate sizes in GB)
    MODEL_HIERARCHY = [
        {"name": "codellama:34b", "size_gb": 20, "priority": 1},
        {"name": "codellama:13b", "size_gb": 7, "priority": 2},
        {"name": "codellama:7b", "size_gb": 4, "priority": 3},
        {"name": "deepseek-coder:6.7b", "size_gb": 4, "priority": 3},
        {"name": "mistral:7b", "size_gb": 4, "priority": 3},
        {"name": "llama2:7b", "size_gb": 4, "priority": 3},
        {"name": "phi:2.7b", "size_gb": 2, "priority": 4},
        {"name": "tinyllama:1.1b", "size_gb": 0.7, "priority": 5},
        {"name": "starcoder:1b", "size_gb": 0.6, "priority": 5},
        {"name": "qwen:0.5b", "size_gb": 0.3, "priority": 6},
    ]
    
    # Required buffer space in GB (for model files, generated code, and temporary files)
    REQUIRED_BUFFER_GB = 2.0
    
    @staticmethod
    def get_available_space_gb(path="."):
        """Get available disk space in GB at the given path"""
        try:
            disk_usage = shutil.disk_usage(path)
            available_gb = disk_usage.free / (1024**3)
            return available_gb
        except Exception as e:
            logger.warning(f"Could not check disk space: {e}")
            return None
    
    @staticmethod
    def get_available_ram_gb():
        """Get available RAM in GB"""
        try:
            mem = psutil.virtual_memory()
            available_ram_gb = mem.available / (1024**3)
            return available_ram_gb
        except Exception as e:
            logger.warning(f"Could not check RAM: {e}")
            return None
    
    @staticmethod
    def select_models_based_on_space(requested_models, available_gb=None, available_ram_gb=None):
        """
        Select appropriate models based on available disk space and RAM.
        Falls back to smaller models if insufficient space.
        """
        if available_gb is None:
            available_gb = DiskSpaceManager.get_available_space_gb()
        
        if available_ram_gb is None:
            available_ram_gb = DiskSpaceManager.get_available_ram_gb()
        
        logger.info(f"System Resources - Disk: {available_gb:.2f} GB free, RAM: {available_ram_gb:.2f} GB available")
        
        if available_gb is None:
            logger.warning("Could not determine disk space, using requested models")
            return requested_models
        
        # Check if we have minimum space for the smallest model
        smallest_model = min(DiskSpaceManager.MODEL_HIERARCHY, key=lambda x: x["size_gb"])
        if available_gb < (smallest_model["size_gb"] + DiskSpaceManager.REQUIRED_BUFFER_GB):
            logger.error(f"Insufficient disk space. Need at least {smallest_model['size_gb'] + DiskSpaceManager.REQUIRED_BUFFER_GB:.1f} GB, but only {available_gb:.1f} GB available")
            return []
        
        # Sort models by priority (lower number = higher priority/larger model)
        sorted_models = sorted(DiskSpaceManager.MODEL_HIERARCHY, key=lambda x: x["priority"])
        
        # Filter to requested models if specified
        if requested_models:
            available_models = [m for m in sorted_models if m["name"] in requested_models]
            if not available_models:
                logger.warning(f"Requested models not in hierarchy, using defaults")
                available_models = sorted_models
        else:
            available_models = sorted_models
        
        # Select models that fit in available space
        selected_models = []
        total_size_gb = 0
        
        for model in available_models:
            model_size = model["size_gb"]
            
            # Check if model fits considering both disk space and RAM
            if (total_size_gb + model_size + DiskSpaceManager.REQUIRED_BUFFER_GB <= available_gb and
                model_size * 1.5 <= available_ram_gb):  # Models need RAM for loading
                
                selected_models.append(model["name"])
                total_size_gb += model_size
                logger.debug(f"Selected model: {model['name']} ({model_size} GB)")
            else:
                logger.debug(f"Skipping model {model['name']} - insufficient space/RAM")
        
        if not selected_models:
            # Try to find at least one model that fits
            for model in reversed(available_models):  # Try smallest first
                if model["size_gb"] + DiskSpaceManager.REQUIRED_BUFFER_GB <= available_gb:
                    selected_models = [model["name"]]
                    logger.info(f"Selected minimal model: {model['name']}")
                    break
        
        logger.info(f"Selected {len(selected_models)} models based on available space: {selected_models}")
        logger.info(f"Estimated total model size: {total_size_gb:.1f} GB")
        
        return selected_models
    
    @staticmethod
    def check_model_availability_with_fallback(model_manager, requested_models):
        """
        Check model availability with automatic fallback to smaller models.
        Returns list of available models that fit in current space.
        """
        logger.info("Checking model availability with automatic space-based fallback...")
        
        # First check available disk space and RAM
        available_gb = DiskSpaceManager.get_available_space_gb()
        available_ram_gb = DiskSpaceManager.get_available_ram_gb()
        
        if available_gb is not None:
            logger.info(f"Disk space available: {available_gb:.2f} GB")
        
        if available_ram_gb is not None:
            logger.info(f"RAM available: {available_ram_gb:.2f} GB")
        
        # Select models based on available space
        space_based_models = DiskSpaceManager.select_models_based_on_space(
            requested_models, available_gb, available_ram_gb
        )
        
        if not space_based_models:
            logger.error("No models can fit in available space!")
            return []
        
        # Now check which of these are actually available via the model manager
        available_models = model_manager.get_available_models()
        logger.info(f"API available models: {available_models}")
        
        # Filter to only models that are both space-appropriate and available
        final_models = [m for m in space_based_models if m in available_models]
        
        if not final_models:
            logger.warning("No space-appropriate models available via API")
            
            # Try to find any available model that fits
            for model in space_based_models:
                # Check if we can pull it
                try:
                    logger.info(f"Attempting to pull model: {model}")
                    model_manager.pull_model(model)
                    final_models = [model]
                    logger.info(f"Successfully pulled model: {model}")
                    break
                except Exception as e:
                    logger.warning(f"Failed to pull model {model}: {e}")
                    continue
        
        if not final_models:
            logger.error("Could not find or pull any suitable models!")
            return []
        
        logger.info(f"Final model selection: {final_models}")
        return final_models


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
            self.disk_manager = DiskSpaceManager()
            logger.info("All components initialized successfully")
    
    """Save each solution as a separate Python file with organized directory structure"""
    def save_individual_solution_files(self, solutions_df: pd.DataFrame, base_dir: Path):
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
                    
                    # FIX INDENTATION: Remove leading/trailing whitespace and fix common indentation issues
                    lines = generated_code.split('\n')
                    if lines:
                        # Find minimum indentation (excluding empty lines)
                        non_empty_lines = [line for line in lines if line.strip()]
                        if non_empty_lines:
                            # Count leading spaces for the first non-empty line
                            first_line = non_empty_lines[0]
                            leading_spaces = len(first_line) - len(first_line.lstrip())
                            
                            # If first line is indented, dedent all lines
                            if leading_spaces > 0:
                                generated_code = '\n'.join(line[leading_spaces:] if len(line) > leading_spaces else line.lstrip() 
                                                          for line in lines)
                    
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
        """Debug model availability with automatic space-based fallback"""
        with DebugTimer("Model Detection with Space-Based Fallback"):
            return DiskSpaceManager.check_model_availability_with_fallback(self.model_manager, models)
    
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
            test_problems = problems # Reduced from 5 to 3 for faster testing
            
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
        """Run complete evaluation pipeline with enhanced debugging and automatic model fallback"""
        logger.info("Starting AI Model Evaluation Pipeline with Enhanced Debugging")
        logger.info("=" * 60)
        
        # Check disk space before starting
        available_gb = DiskSpaceManager.get_available_space_gb()
        if available_gb is not None:
            logger.info(f"Initial disk space available: {available_gb:.2f} GB")
        
        # Configuration
        if models is None:
            models = self.config.get("models.default_models", ["codellama:7b"])
        
        if num_samples is None:
            num_samples = self.config.get("evaluation.num_samples_per_task", 5)
        
        logger.info(f"Requested configuration: {len(models)} models, {num_samples} samples per task")
        
        try:
            # Step 1: Load dataset with debugging
            problems = self.debug_data_loading()
            if not problems:
                logger.error("No problems loaded from dataset!")
                return None, None
            
            # Step 2: Check available models with automatic space-based fallback
            models_to_use = self.debug_model_detection(models)
            if not models_to_use:
                logger.error("No suitable models available for evaluation!")
                logger.info("Try: 1. Freeing up disk space")
                logger.info("     2. Pulling a smaller model: ollama pull tinyllama:1.1b")
                logger.info("     3. Checking if ollama is running: ollama serve")
                return None, None
            
            # Adjust sample size based on available space and number of models
            adjusted_num_samples = self.adjust_sample_size_based_on_space(
                num_samples, len(models_to_use), len(problems)
            )
            
            if adjusted_num_samples < num_samples:
                logger.warning(f"Reduced sample size from {num_samples} to {adjusted_num_samples} due to space constraints")
            
            # Step 3: Generate solutions with debugging
            solutions_df = self.debug_code_generation(problems, models_to_use, adjusted_num_samples)
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
    
    def adjust_sample_size_based_on_space(self, requested_samples: int, num_models: int, num_problems: int) -> int:
        """
        Adjust the sample size based on available disk space.
        Returns the adjusted number of samples per task.
        """
        available_gb = DiskSpaceManager.get_available_space_gb()
        if available_gb is None:
            return requested_samples  # Can't determine space, use requested
        
        # Estimate space needed for generated files
        # Each solution file is approximately 2KB, plus overhead
        estimated_files = num_models * num_problems * requested_samples
        estimated_space_mb = (estimated_files * 5) / 1024  # 5KB per file = MB
        
        # Convert to GB
        estimated_space_gb = estimated_space_mb / 1024
        
        # Check if we have enough space with buffer
        required_buffer_gb = 1.0  # Additional buffer for CSV files, logs, etc.
        
        if estimated_space_gb + required_buffer_gb < available_gb * 0.3:  # Use at most 30% of available space
            return requested_samples  # Enough space
        
        # Calculate maximum samples that fit
        max_samples = int((available_gb * 0.3 - required_buffer_gb) * 1024 * 1024 / (num_models * num_problems * 5))
        max_samples = max(1, min(max_samples, requested_samples))
        
        if max_samples < requested_samples:
            logger.info(f"Space optimization: Reduced samples from {requested_samples} to {max_samples}")
            logger.info(f"Estimated file space: {estimated_space_gb:.3f} GB, Available: {available_gb:.2f} GB")
        
        return max_samples
    
    def print_detailed_summary(self, functional_metrics: dict, comparison_report: pd.DataFrame, results_df: pd.DataFrame):
        """Print comprehensive evaluation summary"""
        logger.info("EVALUATION COMPLETE!")
        logger.info("=" * 60)
        
        # Check final disk space
        available_gb = DiskSpaceManager.get_available_space_gb()
        if available_gb is not None:
            logger.info(f"Final disk space available: {available_gb:.2f} GB")
        
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
    """Main execution function with enhanced error handling and space management"""
    try:
        logger.info("AI Model Evaluation Starting...")
        logger.info("System will automatically select lighter models if space is limited")
        
        # Check initial system resources
        available_gb = DiskSpaceManager.get_available_space_gb()
        available_ram_gb = DiskSpaceManager.get_available_ram_gb()
        
        if available_gb is not None:
            logger.info(f"Initial disk space: {available_gb:.2f} GB")
        if available_ram_gb is not None:
            logger.info(f"Initial RAM available: {available_ram_gb:.2f} GB")
        
        evaluator = AIModelEval()
        
        # Run evaluation with automatic model selection
        logger.info("Starting evaluation with automatic model selection...")
        results, comparison = evaluator.run_full_evaluation(
            models=["codellama:7b", "codellama:13b", "codellama:34b"],  # Will fall back if needed
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