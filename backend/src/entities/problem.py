
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import hashlib
import ast
import radon


class Problem:
    def __init__(
        self,
        task_id: str,
        prompt: str,
        dataset_id: str,
        problem_id: Optional[str] = None
    ):
        self.problem_id = problem_id or self._generate_id(task_id)
        self.task_id = task_id
        self.dataset_id = dataset_id
        self.prompt = prompt
        self.canonical_solution: Optional[str] = None
        self.test_cases: List[Dict[str, Any]] = []
        self.function_signature: Optional[str] = None
        self.entry_point: Optional[str] = None
        self.difficulty: str = "unknown"
        self.categories: List[str] = []
        self.metadata: Dict[str, Any] = {}
        self.created_at = datetime.now()
        self.stats: Dict[str, Any] = {}

    def _generate_id(self, task_id: str) -> str:
        """Generate a unique problem ID"""
        hash_obj = hashlib.md5(task_id.encode())
        return f"prob_{hash_obj.hexdigest()[:8]}"

    def set_canonical_solution(self, solution: str) -> None:
        """Set the canonical solution"""
        self.canonical_solution = solution
        self._extract_function_info()

    def _extract_function_info(self) -> None:
        """Extract function information from solution"""
        if not self.canonical_solution:
            return
        
        try:
            tree = ast.parse(self.canonical_solution)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.function_signature = ast.unparse(node)
                    self.entry_point = node.name
                    break
        except Exception:
            pass

    def add_test_case(self, test_case: Dict[str, Any]) -> None:
        """Add a test case"""
        self.test_cases.append(test_case)

    def set_test_cases(self, test_code: str) -> None:
        """Parse and set test cases from test code"""
        # Parse assert statements from test code
        lines = test_code.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('assert'):
                self.test_cases.append({
                    'assertion': line,
                    'type': 'assert'
                })

    def get_prompt(self, include_signature: bool = True) -> str:
        """Get the problem prompt"""
        if include_signature and self.function_signature:
            return f"{self.prompt}\n\n# Complete the function:\n{self.function_signature}"
        return self.prompt

    def run_tests(self, code: str) -> List[Dict[str, Any]]:
        """Run test cases against provided code"""
        results = []
        test_globals = {}
        
        try:
            # Execute the code
            exec(code, test_globals)
            
            # Run each test case
            for i, test in enumerate(self.test_cases):
                try:
                    if 'assertion' in test:
                        exec(test['assertion'], test_globals)
                        results.append({
                            'test_id': i,
                            'passed': True,
                            'message': f'Test {i+1} passed'
                        })
                except AssertionError as e:
                    results.append({
                        'test_id': i,
                        'passed': False,
                        'message': f'Test {i+1} failed: {str(e)}',
                        'assertion': test.get('assertion')
                    })
                except Exception as e:
                    results.append({
                        'test_id': i,
                        'passed': False,
                        'message': f'Test {i+1} error: {str(e)}',
                        'assertion': test.get('assertion')
                    })
                    
        except Exception as e:
            results.append({
                'test_id': 0,
                'passed': False,
                'message': f'Code execution failed: {str(e)}'
            })
        
        return results

    def validate_solution(self, code: str) -> bool:
        """Validate if code passes all tests"""
        results = self.run_tests(code)
        return all(r.get('passed', False) for r in results)

    def calculate_complexity(self) -> Dict[str, Any]:
        """Calculate code complexity metrics"""
        if not self.canonical_solution:
            return {}
        
        try:
            from radon.raw import analyze
            from radon.complexity import cc_visit
            
            raw = analyze(self.canonical_solution)
            cc = cc_visit(self.canonical_solution)
            
            return {
                'loc': raw.loc,
                'lloc': raw.lloc,
                'comments': raw.comments,
                'cyclomatic_complexity': sum(c.complexity for c in cc) / len(cc) if cc else 0,
                'functions': len(cc)
            }
        except Exception:
            return {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert problem to dictionary"""
        return {
            'problem_id': self.problem_id,
            'task_id': self.task_id,
            'dataset_id': self.dataset_id,
            'prompt': self.prompt,
            'canonical_solution': self.canonical_solution,
            'test_cases': self.test_cases,
            'function_signature': self.function_signature,
            'entry_point': self.entry_point,
            'difficulty': self.difficulty,
            'categories': self.categories,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'stats': self.stats or self.calculate_complexity()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Problem':
        """Create problem from dictionary"""
        problem = cls(
            task_id=data['task_id'],
            prompt=data['prompt'],
            dataset_id=data['dataset_id'],
            problem_id=data.get('problem_id')
        )
        problem.canonical_solution = data.get('canonical_solution')
        problem.test_cases = data.get('test_cases', [])
        problem.function_signature = data.get('function_signature')
        problem.entry_point = data.get('entry_point')
        problem.difficulty = data.get('difficulty', 'unknown')
        problem.categories = data.get('categories', [])
        problem.metadata = data.get('metadata', {})
        problem.created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        problem.stats = data.get('stats', {})
        return problem