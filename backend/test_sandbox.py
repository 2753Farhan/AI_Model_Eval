# test_final_complete.py
"""
Complete fix for all 164 problems
Run: python test_final_complete.py
"""

import asyncio
import sys
import os
import json
import gzip
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union, Set

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.executors import SandboxExecutor


class CompleteTester:
    """Complete fix for all problems"""
    
    def __init__(self):
        self.sandbox = SandboxExecutor(
            timeout=30,
            memory_limit="512m",
            cpu_limit=1.0,
            network_enabled=False
        )
        self.stats = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': []
        }
        self.start_time = datetime.now()
    
    def load_all_problems(self):
        """Load all 164 problems"""
        data_file = "data/data/HumanEval.jsonl.gz"
        if not Path(data_file).exists():
            print(f"❌ Data file not found: {data_file}")
            return []
        
        problems = []
        try:
            with gzip.open(data_file, 'rt', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    problems.append({
                        'task_id': data.get('task_id'),
                        'prompt': data.get('prompt', ''),
                        'canonical_solution': data.get('canonical_solution', ''),
                        'test': data.get('test', ''),
                        'entry_point': data.get('entry_point'),
                    })
            
            print(f"✅ Loaded {len(problems)} problems")
            return problems
        except Exception as e:
            print(f"❌ Error loading: {e}")
            return []
    
    def extract_signature(self, prompt: str, entry_point: str) -> str:
        """Extract function signature from prompt"""
        for line in prompt.split('\n'):
            if line.strip().startswith('def ' + entry_point):
                return line.rstrip()
        return f"def {entry_point}(*args, **kwargs):"
    
    def add_all_imports(self) -> str:
        """Add ALL possible imports that might be needed"""
        return """import math
import copy
import random
import itertools
import collections
import re
import sys
import json
import hashlib
import functools
import operator
from typing import List, Dict, Tuple, Optional, Set, Any, Union, Callable
from collections import defaultdict, Counter, deque
from functools import reduce, lru_cache
from itertools import permutations, combinations, product

"""
    
    def extract_test_cases(self, test_code: str, entry_point: str) -> List[Dict]:
        """Extract test cases correctly"""
        test_cases = []
        
        for line in test_code.split('\n'):
            line = line.strip()
            if line.startswith('assert'):
                # Replace 'candidate' with function name
                assertion = line.replace('candidate', entry_point)
                test_cases.append({'assertion': assertion})
        
        return test_cases
    
    def build_complete_function(self, problem: Dict) -> str:
        """Build complete function with ALL fixes"""
        entry_point = problem['entry_point']
        prompt = problem['prompt']
        body = problem['canonical_solution']
        
        # Extract signature
        signature = self.extract_signature(prompt, entry_point)
        
        # Handle special case where body might be indented
        if body and not body[0].isspace():
            # Body is not indented, add 4 spaces
            indented_body = '\n'.join('    ' + line if line.strip() else line 
                                      for line in body.split('\n'))
        else:
            # Body already has correct indentation
            indented_body = body
        
        # Combine signature + body
        complete_function = f"{signature}\n{indented_body}"
        
        # Add ALL imports at the top
        complete_function = self.add_all_imports() + complete_function
        
        return complete_function
    
    async def test_problem(self, problem: Dict, index: int, total: int):
        """Test a single problem"""
        self.stats['total'] += 1
        
        print(f"\r  Testing: {index}/{total} - {problem['task_id'][:30]:30} ", end='', flush=True)
        
        # Build function with ALL fixes
        complete_function = self.build_complete_function(problem)
        
        # Extract test cases
        test_cases = self.extract_test_cases(problem['test'], problem['entry_point'])
        
        # Execute
        result = await self.sandbox.execute_safely(
            code=complete_function,
            test_cases=test_cases,
            problem_id=problem['task_id'],
            language="python"
        )
        
        if result.get('passed', False):
            self.stats['passed'] += 1
        else:
            self.stats['failed'] += 1
            if len(self.stats['errors']) < 20:
                error_msg = result.get('output', 'Unknown')
                # Clean up error message
                if len(error_msg) > 200:
                    error_msg = error_msg[:200] + "..."
                self.stats['errors'].append({
                    'task_id': problem['task_id'],
                    'error': error_msg
                })
    
    def print_summary(self):
        """Print summary"""
        elapsed = datetime.now() - self.start_time
        
        print("\n\n" + "=" * 70)
        print("COMPLETE TEST RESULTS")
        print("=" * 70)
        print(f"⏱️  Time: {elapsed.total_seconds():.1f}s")
        print(f"📊 Total: {self.stats['total']}")
        print(f"✅ Passed: {self.stats['passed']}")
        print(f"❌ Failed: {self.stats['failed']}")
        
        if self.stats['total'] > 0:
            rate = (self.stats['passed'] / self.stats['total']) * 100
            print(f"📈 Pass rate: {rate:.1f}%")
        
        if self.stats['errors']:
            print(f"\n❌ Remaining errors ({len(self.stats['errors'])}):")
            for i, err in enumerate(self.stats['errors']):
                print(f"  {i+1}. {err['task_id']}: {err['error'][:100]}")
    
    def cleanup(self):
        """Clean up"""
        self.sandbox.cleanup()
        print(f"\n✅ Cleanup complete")


async def main():
    """Main entry point"""
    print("=" * 70)
    print("COMPLETE FIX - ALL 164 PROBLEMS")
    print("=" * 70)
    print("Fixes applied:")
    print("  • ALL typing imports (List, Dict, Tuple, Optional, Any, etc.)")
    print("  • Standard library imports (math, copy, random, etc.)")
    print("  • Proper indentation handling")
    print("  • Test case extraction")
    
    tester = CompleteTester()
    problems = tester.load_all_problems()
    
    if not problems:
        return 1
    
    print(f"\n🧪 Testing {len(problems)} problems...\n")
    
    # Test all problems
    for i, problem in enumerate(problems, 1):
        await tester.test_problem(problem, i, len(problems))
    
    # Print summary
    tester.print_summary()
    
    # Save results
    results_file = f"test_results_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump({
            'stats': tester.stats,
            'timestamp': str(datetime.now())
        }, f, indent=2)
    print(f"\n💾 Results saved to {results_file}")
    
    tester.cleanup()
    
    return 0 if tester.stats['failed'] == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)