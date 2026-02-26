# test.py - Updated with cleanup
"""
Quick test script to verify evaluation works with minimal samples
Run: python test.py
"""

import asyncio
import sys
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.append(str(Path(__file__).parent))

async def quick_test():
    """Run a quick test with just 1-2 problems"""
    
    print("\n" + "="*60)
    print("QUICK EVALUATION TEST")
    print("="*60)
    
    model = None  # Initialize model variable
    
    try:
        # Import required modules
        from src.adapters import ModelRegistry
        from src.loaders import HumanEvalLoader
        from src.executors import SandboxExecutor
        from src.calculators import FunctionalMetricsCalculator, QualityMetricsCalculator
        from src.analyzers import ErrorAnalyzer
        from src.managers import EvaluationManager
        from src.config.config_manager import ConfigManager
        from src.entities import EvaluationResult
        
        print("\n1. Initializing components...")
        
        # Initialize config
        config = ConfigManager("config/settings.yaml")
        
        # Initialize model registry
        model_registry = ModelRegistry()
        model_registry.load_from_config(config.config)
        
        # Initialize dataset loader
        dataset_loader = HumanEvalLoader({
            'repo_url': config.get('paths.repo_url'),
            'data_dir': config.get('paths.data_dir'),
            'name': 'HumanEval'
        })
        
        # Initialize sandbox
        sandbox = SandboxExecutor(
            timeout=config.get('evaluation.timeout_seconds', 30),
            memory_limit=f"{config.get('evaluation.max_memory_mb', 512)}m"
        )
        
        # Initialize calculators
        metric_calculator = FunctionalMetricsCalculator()
        quality_calculator = QualityMetricsCalculator({})
        error_analyzer = ErrorAnalyzer()
        
        # Initialize manager
        evaluation_manager = EvaluationManager(
            model_registry=model_registry,
            dataset_loader=dataset_loader,
            sandbox_executor=sandbox,
            metric_calculator=metric_calculator,
            error_analyzer=error_analyzer,
            max_workers=1
        )
        
        print("✅ Components initialized")
        
        print("\n2. Loading dataset...")
        problems = dataset_loader.load_dataset()
        print(f"✅ Loaded {len(problems)} problems total")
        
        # Take first 2 problems
        test_problems = problems[:2]
        print(f"✅ Testing with {len(test_problems)} problems: {[p.problem_id for p in test_problems]}")
        
        print("\n3. Getting model...")
        model = model_registry.get_model("codellama:7b")
        if not model:
            print("❌ Model not found!")
            return
        print("✅ Model loaded")
        
        print("\n4. Running evaluation on 2 problems (1 sample each)...")
        print("-" * 40)
        
        results = []
        
        for i, problem in enumerate(test_problems):
            print(f"\n   Problem {i+1}: {problem.problem_id}")
            print(f"   Entry point: {problem.entry_point}")
            
            # Generate code
            print("   Generating code...")
            generated_code = await model.generate_code(problem.prompt)
            print(f"   Generated {len(generated_code)} chars")
            
            if len(generated_code) > 50:
                preview = generated_code[:100].replace('\n', ' ').strip()
                print(f"   Preview: {preview[:100]}...")
            
            # Execute
            print("   Executing...")
            execution_result = await sandbox.execute_safely(
                generated_code,
                problem.test_cases,
                problem.problem_id,
                language="python",
                entry_point=problem.entry_point,
                prompt=problem.prompt
            )
            
            # Create result
            result = EvaluationResult(
                evaluation_id="test",
                problem_id=problem.problem_id,
                model_id="codellama:7b",
                sample_id=0
            )
            result.set_generated_code(generated_code)
            result.set_execution_result(
                passed=execution_result.get('passed', False),
                output=execution_result.get('output', ''),
                execution_time_ms=execution_result.get('execution_time_ms', 0)
            )
            
            # Add test results
            for test in execution_result.get('test_results', []):
                result.add_test_result(
                    test_id=test.get('test_id', 0),
                    passed=test.get('passed', False),
                    message=test.get('message', '')
                )
            
            results.append(result)
            
            print(f"   Result: {'✅ PASSED' if result.passed else '❌ FAILED'}")
            if result.execution_time_ms:
                print(f"   Time: {result.execution_time_ms:.2f}ms")
        
        print("\n" + "="*40)
        print("RESULTS SUMMARY")
        print("="*40)
        
        passed = sum(1 for r in results if r.passed)
        print(f"Total: {len(results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {len(results) - passed}")
        print(f"Pass Rate: {passed/len(results)*100:.1f}%")
        
        print("\n" + "="*40)
        print("TESTING METRICS CALCULATION")
        print("="*40)
        
        # Test calculate_aggregate_metrics
        print("\nTesting FunctionalMetricsCalculator.calculate_aggregate_metrics():")
        try:
            if hasattr(metric_calculator, 'calculate_aggregate_metrics'):
                agg_metrics = metric_calculator.calculate_aggregate_metrics(results)
                print(f"✅ Method exists!")
                print(f"   Metrics: {agg_metrics}")
            else:
                print("❌ Method missing!")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*40)
        print("TEST COMPLETE")
        print("="*40)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # CLEANUP
        print("\n" + "="*40)
        print("CLEANING UP")
        print("="*40)
        
        # Close model session
        if model and hasattr(model, 'close'):
            try:
                await model.close()
                print("✅ Closed model session")
            except:
                pass
        
        # Close sandbox
        if 'sandbox' in locals() and hasattr(sandbox, 'cleanup'):
            try:
                sandbox.cleanup()
                print("✅ Cleaned up sandbox")
            except:
                pass
        
        # Close aiohttp sessions
        try:
            import aiohttp
            for task in asyncio.all_tasks():
                if task is not asyncio.current_task():
                    task.cancel()
            print("✅ Cancelled pending tasks")
        except:
            pass
        
        print("✅ Cleanup complete")

if __name__ == "__main__":
    asyncio.run(quick_test())