# main.py (updated with --analyze flag)
import os
import sys
import asyncio
import logging
import argparse
import json
from pathlib import Path
from typing import Optional
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

# Fix imports - use absolute imports
from src.entities import User, Evaluation, Report, EvaluationResult, Benchmark
from src.managers import EvaluationManager, ResultAggregator
from src.adapters import ModelRegistry
from src.loaders import HumanEvalLoader
from src.executors import SandboxExecutor, ResourceManager
from src.calculators import (
    MetricCalculator,
    FunctionalMetricsCalculator,
    QualityMetricsCalculator,
    SemanticMetricsCalculator
)
from src.analyzers import ErrorAnalyzer, PatternDetector, FixSuggester
from src.generators import ReportGenerator
from src.prompts import PromptEngine
from src.utils import DiskSpaceManager, DebugTimer, Validators
from src.config.config_manager import ConfigManager

# Import the new analyzer
from src.analyzers.dataset_analyzer import DatasetAnalyzer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_modeleval.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class CombinedMetricCalculator(MetricCalculator):
    """Combines multiple metric calculators into one"""
    
    def __init__(self, config: Optional[dict] = None):
        super().__init__(config or {})
        self.functional = FunctionalMetricsCalculator(config)
        self.quality = QualityMetricsCalculator(config)
        self.semantic = SemanticMetricsCalculator(config)
        
        # Combine supported metrics
        self.supported_metrics = (
            self.functional.supported_metrics +
            self.quality.supported_metrics +
            self.semantic.supported_metrics
        )
        
        # Combine normalization rules
        self.normalization_rules.update(self.functional.normalization_rules)
        self.normalization_rules.update(self.quality.normalization_rules)
        self.normalization_rules.update(self.semantic.normalization_rules)
        
        # Combine thresholds
        self.thresholds.update(self.functional.thresholds)
        self.thresholds.update(self.quality.thresholds)
        self.thresholds.update(self.semantic.thresholds)
        
        # Combine weights
        self.weights.update(self.functional.weights)
        self.weights.update(self.quality.weights)
        self.weights.update(self.semantic.weights)
    
    def calculate(self, results):
        """Calculate all metrics"""
        metrics = {}
        
        # Calculate from each calculator
        if self.functional:
            metrics.update(self.functional.calculate(results))
        if self.quality:
            metrics.update(self.quality.calculate(results))
        if self.semantic:
            metrics.update(self.semantic.calculate(results))
        
        return metrics
    
    def calculate_for_result(self, result):
        """Calculate metrics for a single result"""
        metrics = {}
        
        if self.functional:
            metrics.update(self.functional.calculate_for_result(result))
        if self.quality:
            metrics.update(self.quality.calculate_for_result(result))
        if self.semantic:
            metrics.update(self.semantic.calculate_for_result(result))
        
        return metrics
    
    def calculate_aggregate_metrics(self, results):
        """Calculate aggregate metrics across all results"""
        return {
            'functional': self.functional.calculate(results) if self.functional else {},
            'quality': self.quality.calculate(results) if self.quality else {},
            'semantic': self.semantic.calculate(results) if self.semantic else {}
        }


class AI_ModelEval:
    """Main application class for AI_ModelEval"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        with DebugTimer("Initialization"):
            logger.info("Initializing AI_ModelEval...")
            
            # Load configuration
            self.config = ConfigManager(config_path)
            self.config.ensure_dirs()
            
            # Initialize utilities
            self.disk_manager = DiskSpaceManager()
            
            # Initialize components
            self._init_components()
            
            logger.info("AI_ModelEval initialized successfully")

    def _init_components(self):
        """Initialize all components"""
        # Model registry
        self.model_registry = ModelRegistry()
        self.model_registry.load_from_config(self.config.config)
        
        # Dataset loaders
        self.dataset_loader = HumanEvalLoader({
            'repo_url': self.config.get('paths.repo_url'),
            'data_dir': self.config.get('paths.data_dir'),
            'name': 'HumanEval'
        })
        
        # Executors
        self.resource_manager = ResourceManager()
        self.sandbox = SandboxExecutor(
            timeout=self.config.get('evaluation.timeout_seconds', 30),
            memory_limit=f"{self.config.get('evaluation.max_memory_mb', 512)}m"
        )
        
        # Get analyzer config from main config
        analyzer_config = self.config.get('analyzers', {})
        
        # Calculators - Use concrete implementations
        self.functional_metrics = FunctionalMetricsCalculator(self.config.get('metrics', {}))
        self.quality_metrics = QualityMetricsCalculator(self.config.get('metrics', {}))
        self.semantic_metrics = SemanticMetricsCalculator(self.config.get('metrics', {}))
        
        # Create combined calculator for EvaluationManager
        self.metric_calculator = CombinedMetricCalculator(self.config.get('metrics', {}))
        
        # Analyzers - Pass config dictionary (not None)
        self.error_analyzer = ErrorAnalyzer(analyzer_config)
        self.pattern_detector = PatternDetector(analyzer_config)
        self.fix_suggester = FixSuggester(analyzer_config)
        
        # Generators
        self.report_generator = ReportGenerator({
            'output_dir': self.config.get('paths.results_dir')
        })
        
        # Prompts
        self.prompt_engine = PromptEngine(self.config.get('prompts', {}))
        
        # Managers
        self.evaluation_manager = EvaluationManager(
            model_registry=self.model_registry,
            dataset_loader=self.dataset_loader,
            sandbox_executor=self.sandbox,
            metric_calculator=self.metric_calculator,
            error_analyzer=self.error_analyzer,
            max_workers=self.config.get('evaluation.resource_limits.max_concurrent', 4)
        )
        
        self.result_aggregator = ResultAggregator()

    async def run_evaluation(
        self,
        model_ids: Optional[list] = None,
        num_samples: Optional[int] = None,
        dataset_id: Optional[str] = None,
        test_mode: bool = False
    ) -> Evaluation:
        """Run a complete evaluation"""
        logger.info("Starting evaluation pipeline...")

        # Check disk space
        available_gb = self.disk_manager.get_available_space_gb()
        if available_gb and available_gb < 10:
            logger.warning(f"Low disk space: {available_gb:.2f} GB")
            recommendations = self.disk_manager.get_cleanup_recommendations()
            for rec in recommendations:
                logger.warning(f"  - {rec['action']} ({rec['size_gb']:.1f} GB)")

        # Use default models if not specified
        if not model_ids:
            model_ids = self.config.get('models.default_models', ['codellama:7b'])

        # Check model availability
        available_models, space_info = self.disk_manager.check_model_availability(
            self.model_registry, model_ids
        )

        if not available_models:
            logger.error("No suitable models available")
            return None

        logger.info(f"Using models: {available_models}")

        # Load dataset FIRST (only once)
        if not dataset_id:
            # Load the full dataset
            problems = self.dataset_loader.load_dataset()
            logger.info(f"[DEBUG] Loaded {len(problems)} total problems")
            
            # NOW apply test mode if enabled - this modifies the loaded dataset
            if test_mode:
                # Store original problems
                self._original_problems = problems.copy()
                # Limit to first 5
                self.dataset_loader.problems = problems[:5]
                # CRITICAL FIX: Update the evaluation manager's loader
                self.evaluation_manager.dataset_loader = self.dataset_loader
                logger.info(f"[TEST MODE] Limited to {len(self.dataset_loader.problems)} problems")
            
            dataset_id = self.dataset_loader.dataset_id

        # Final debug check
        logger.info(f"[DEBUG] Final dataset size: {len(self.dataset_loader.problems)} problems")

        # Create evaluation
        evaluation = self.evaluation_manager.create_evaluation(
            user_id='system',
            model_ids=available_models,
            dataset_id=dataset_id,
            config={
                'num_samples': num_samples or self.config.get('evaluation.num_samples_per_task', 5),
                'strategies': self.config.get('evaluation.prompt_strategies', ['zero_shot']),
                'timeout': self.config.get('evaluation.timeout_seconds', 30)
            }
        )

        # Run evaluation
        def progress_callback(eval_id, stage, message, data):
            logger.info(f"[{stage}] {message}")
            if data and 'progress' in data:
                print(f"Progress: {data['progress']:.1f}%")

        evaluation = await self.evaluation_manager.run_evaluation(
            evaluation.evaluation_id,
            progress_callback
        )

        # Get results
        results = self.evaluation_manager.get_results(evaluation.evaluation_id)

        # AUTO-SAVE RESULTS TO DISK
        await self._save_results_to_disk(evaluation, results)

        # Aggregate results
        self.result_aggregator.add_results(evaluation.evaluation_id, results)

        # Generate report
        try:
            report = self.report_generator.generate_summary_report(
                evaluation,
                results,
                format='html'
            )
            logger.info(f"[SAVED] Report to: {report.file_path}")
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            fallback_path = Path("results") / f"raw_results_{evaluation.evaluation_id}.json"
            with open(fallback_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'evaluation_id': evaluation.evaluation_id,
                    'results': [r.to_dict() for r in results]
                }, f, indent=2, default=str)
            logger.info(f"[SAVED] Raw results to: {fallback_path}")

        # Print summary
        passed = sum(1 for r in results if r.passed)
        total = len(results)
        logger.info(f"[RESULTS] Evaluation complete: {passed}/{total} passed ({passed/total*100:.1f}%)")

        # Restore full dataset if test mode was enabled
        if test_mode and hasattr(self, '_original_problems'):
            self.dataset_loader.problems = self._original_problems
            self.evaluation_manager.dataset_loader = self.dataset_loader
            logger.info("[TEST MODE] Restored full dataset")

        return evaluation

    async def _save_results_to_disk(self, evaluation, results):
        """Save results to disk in multiple formats"""
        try:
            # Create results directory
            results_dir = Path("results")
            results_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            eval_id = evaluation.evaluation_id
            
            # 1. Save as JSON (full data)
            json_path = results_dir / f"eval_{eval_id}_{timestamp}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'evaluation_id': eval_id,
                    'timestamp': timestamp,
                    'model_ids': evaluation.model_ids,
                    'config': evaluation.config,
                    'total_results': len(results),
                    'passed': sum(1 for r in results if r.passed),
                    'failed': sum(1 for r in results if not r.passed),
                    'results': [r.to_dict() for r in results]
                }, f, indent=2, default=str)
            logger.info(f"[SAVED] JSON to: {json_path}")
            
            # 2. Save as CSV (summary)
            csv_path = results_dir / f"summary_{eval_id}_{timestamp}.csv"
            with open(csv_path, 'w', encoding='utf-8') as f:
                f.write("problem_id,model_id,sample_id,passed,execution_time_ms,error_count\n")
                for r in results:
                    f.write(f"{r.problem_id},{r.model_id},{r.sample_id},{r.passed},{r.execution_time_ms or 0},{len(r.errors)}\n")
            logger.info(f"[SAVED] CSV to: {csv_path}")
            
            # 3. Save simple text summary
            txt_path = results_dir / f"summary_{eval_id}_{timestamp}.txt"
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(f"Evaluation Results\n")
                f.write(f"=" * 50 + "\n")
                f.write(f"Evaluation ID: {eval_id}\n")
                f.write(f"Date: {timestamp}\n")
                f.write(f"Models: {', '.join(evaluation.model_ids)}\n")
                f.write(f"Total Samples: {len(results)}\n")
                f.write(f"Passed: {sum(1 for r in results if r.passed)}\n")
                f.write(f"Failed: {sum(1 for r in results if not r.passed)}\n")
                f.write(f"Pass Rate: {sum(1 for r in results if r.passed)/len(results)*100:.1f}%\n")
            logger.info(f"[SAVED] Summary to: {txt_path}")
            
        except Exception as e:
            logger.error(f"Failed to save results to disk: {e}")

    async def analyze_dataset(self, data_path: str = None, limit: int = None):
        """Run dataset analysis"""
        logger.info("Starting dataset analysis...")
        
        # Create analyzer
        analyzer = DatasetAnalyzer(sandbox=self.sandbox)
        
        # Load dataset
        if not data_path:
            data_path = "data/data/HumanEval.jsonl.gz"
        
        logger.info(f"Loading dataset from {data_path}...")
        if not analyzer.load_dataset(data_path):
            logger.error("Failed to load dataset")
            return False
        
        # Run analysis
        logger.info(f"Analyzing {'all' if not limit else limit} problems...")
        await analyzer.analyze_all(limit=limit)
        
        # Print summary
        analyzer.print_summary()
        
        # Generate reports
        logger.info("Generating visualizations and reports...")
        analyzer.generate_report()
        
        # Get failing tests
        failing = analyzer.get_failing_tests()
        if failing:
            logger.info(f"\n❌ {len(failing)} Failing Tests:")
            for test in failing[:10]:
                logger.info(f"  • {test['task_id']}: {test['error_type']}")
        
        # Get slow tests
        slow = analyzer.get_slow_tests(threshold_ms=1000)
        if slow:
            logger.info(f"\n🐢 {len(slow)} Slow Tests (>1s):")
            for test in slow[:5]:
                logger.info(f"  • {test['task_id']}: {test['time_ms']:.0f}ms")
        
        analyzer.cleanup()
        return True

    def start_dashboard(self, host: str = None, port: int = None):
        """Start the dashboard server"""
        from src.dashboard.app import create_app
        
        app = create_app()
        app.run(
            host=host or self.config.get('dashboard.host', '0.0.0.0'),
            port=port or self.config.get('dashboard.port', 5000),
            debug=self.config.get('dashboard.debug', False)
        )

    def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up...")
        
        # Stop resource monitoring
        self.resource_manager.stop_monitoring()
        
        # Close model connections
        asyncio.run(self.model_registry.close_all())
        
        # Clean up sandbox
        self.sandbox.cleanup()
        
        logger.info("Cleanup complete")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='AI_ModelEval - Evaluate AI Code Models')
    parser.add_argument('--config', type=str, default='config/settings.yaml',
                       help='Configuration file path')
    parser.add_argument('--mode', type=str, 
                       choices=['eval', 'dashboard', 'benchmark', 'analyze'],
                       default='dashboard', help='Operation mode')
    parser.add_argument('--models', type=str, nargs='+',
                       help='Models to evaluate')
    parser.add_argument('--samples', type=int, default=5,
                       help='Number of samples per task')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                       help='Dashboard host')
    parser.add_argument('--port', type=int, default=5000,
                       help='Dashboard port')
    parser.add_argument('--test', action='store_true',
                       help='Test mode - only run first 5 problems')
    
    # Dataset analysis arguments
    parser.add_argument('--analyze', action='store_true',
                       help='Run dataset analysis (use with --mode analyze)')
    parser.add_argument('--data-path', type=str, default='data/data/HumanEval.jsonl.gz',
                       help='Path to dataset file for analysis')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit number of problems to analyze')
    
    args = parser.parse_args()
    
    # Create application
    app = AI_ModelEval(config_path=args.config)
    
    try:
        if args.mode == 'eval':
            # Run evaluation
            logger.info(f"Starting evaluation with models: {args.models}")
            if args.test:
                logger.info("[TEST MODE] Will only run first 5 problems")
            
            asyncio.run(app.run_evaluation(
                model_ids=args.models,
                num_samples=args.samples,
                test_mode=args.test
            ))
            
        elif args.mode == 'dashboard':
            # Start dashboard
            logger.info(f"Starting dashboard on {args.host}:{args.port}")
            app.start_dashboard(host=args.host, port=args.port)
            
        elif args.mode == 'benchmark':
            # Run benchmark
            logger.info("Benchmark mode not yet implemented")
            
        elif args.mode == 'analyze':
            # Run dataset analysis
            logger.info("Running dataset analysis...")
            asyncio.run(app.analyze_dataset(
                data_path=args.data_path,
                limit=args.limit
            ))
            
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        app.cleanup()


if __name__ == '__main__':
    main()