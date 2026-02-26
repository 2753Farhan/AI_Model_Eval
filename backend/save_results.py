# save_results.py
import asyncio
import json
import pickle
from pathlib import Path
from datetime import datetime
from main import AI_ModelEval

async def save_results():
    print("Loading AI ModelEval...")
    app = AI_ModelEval()
    
    # Find the latest evaluation
    eval_id = None
    for eid, eval_obj in app.evaluation_manager.evaluations.items():
        eval_id = eid
        print(f"Found evaluation: {eval_id}")
        break
    
    if not eval_id:
        print("No evaluations found!")
        return
    
    # Get evaluation and results
    evaluation = app.evaluation_manager.get_evaluation(eval_id)
    results = app.evaluation_manager.get_results(eval_id)
    
    print(f"Evaluation: {evaluation.evaluation_id}")
    print(f"Total results: {len(results)}")
    print(f"Passed: {sum(1 for r in results if r.passed)}")
    print(f"Failed: {sum(1 for r in results if not r.passed)}")
    
    # Create results directory if it doesn't exist
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save as JSON
    json_path = results_dir / f"evaluation_{eval_id}_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump({
            'evaluation_id': eval_id,
            'model_ids': evaluation.model_ids,
            'total_results': len(results),
            'passed': sum(1 for r in results if r.passed),
            'failed': sum(1 for r in results if not r.passed),
            'results': [r.to_dict() for r in results]
        }, f, indent=2, default=str)
    print(f"✅ Saved JSON to: {json_path}")
    
    # Save summary as CSV
    csv_path = results_dir / f"summary_{eval_id}_{timestamp}.csv"
    with open(csv_path, 'w') as f:
        f.write("problem_id,passed,execution_time_ms,error_count\n")
        for r in results:
            error_count = len(r.errors)
            f.write(f"{r.problem_id},{r.passed},{r.execution_time_ms or 0},{error_count}\n")
    print(f"✅ Saved CSV to: {csv_path}")
    
    # Try to generate HTML report (after fixing report.py)
    try:
        report = app.report_generator.generate_summary_report(
            evaluation, results, format='html'
        )
        print(f"✅ Saved HTML report to: {report.file_path}")
    except Exception as e:
        print(f"⚠️ HTML report failed: {e}")
    
    # Print some statistics
    print("\n📊 Statistics:")
    print(f"  Total samples: {len(results)}")
    print(f"  Passed: {sum(1 for r in results if r.passed)}")
    print(f"  Failed: {sum(1 for r in results if not r.passed)}")
    pass_rate = sum(1 for r in results if r.passed) / len(results) * 100
    print(f"  Pass rate: {pass_rate:.1f}%")
    
    # Average execution time
    exec_times = [r.execution_time_ms for r in results if r.execution_time_ms]
    if exec_times:
        avg_time = sum(exec_times) / len(exec_times)
        print(f"  Avg execution time: {avg_time:.2f}ms")
    
    print(f"\n✅ Results saved to: {results_dir.absolute()}")

if __name__ == "__main__":
    asyncio.run(save_results())