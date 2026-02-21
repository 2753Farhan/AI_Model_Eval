import docker
import logging
import os
import tempfile
import textwrap
import ast
import threading
import queue
import json
import re
from typing import Dict, List

logger = logging.getLogger(__name__)

class SandboxExecutor:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.client = None
        self.setup_docker()
    
    def setup_docker(self):
        """Initialize Docker client"""
        try:
            self.client = docker.from_env()
            logger.info("Docker client initialized")
        except Exception as e:
            logger.warning(f"Docker not available: {e}. Using fallback execution.")
            self.client = None
    
    def execute_safely(self, code: str, tests: str, problem_id: str) -> Dict:
        """Execute code in a safe environment and return results"""
        logger.info(f"Docker client available: {self.client is not None}")
        
        if self.client:
            logger.info("Choosing Docker execution path")
            return self._execute_with_docker_individual_tests(code, tests, problem_id)
        
        logger.info("Docker not available, using fallback")
        return self._execute_with_fallback(code, tests, problem_id)
    
    def _extract_function_name(self, code: str) -> str:
        """Extract the first function name from Python code"""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    logger.debug(f"Extracted function name via AST: {node.name}")
                    return node.name
        except Exception as e:
            logger.debug(f"AST parse failed, trying string scan: {e}")
        
        # Fallback: try to find function definition by scanning
        lines = code.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('def '):
                # Extract function name from "def function_name("
                func_decl = line[4:]  # Remove 'def '
                if '(' in func_decl:
                    func_name = func_decl.split('(')[0].strip()
                    logger.debug(f"Extracted function name via scanning: {func_name}")
                    return func_name
        
        logger.warning("Could not extract function name, using 'candidate'")
        return "candidate"
    
    def _parse_test_cases(self, tests: str, function_name: str) -> List[str]:
        """Parse individual test cases from HumanEval test code"""
        test_cases = []
        lines = tests.strip().split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            # Look for assert statements that use the function
            if line.startswith('assert') and function_name in line:
                # Clean up the assert statement
                if '#' in line:
                    line = line.split('#')[0].strip()
                test_cases.append(line)
        
        return test_cases
    
    def _create_individual_test_program(self, code: str, tests: str, function_name: str) -> str:
        """Create a test program that runs each test case individually"""
        # Parse test cases
        test_cases = self._parse_test_cases(tests, function_name)
        
        if not test_cases:
            # Fallback to original test format
            return f"""
{code}

{tests}

# Run the test
import sys
try:
    check({function_name})
    print("RESULT: PASSED")
    print("TEST_RESULTS: []")
    sys.exit(0)
except AssertionError as e:
    print(f"RESULT: FAILED: {{e}}")
    print("TEST_RESULTS: []")
    sys.exit(1)
except Exception as e:
    print(f"RESULT: ERROR: {{e}}")
    print("TEST_RESULTS: []")
    sys.exit(2)
"""
        
        # Create individual test functions
        test_functions = ""
        for i, test_case in enumerate(test_cases):
            test_functions += f"""
def test_{i}():
    try:
        {test_case}
        return True, "Test {i+1} passed"
    except AssertionError as e:
        return False, f"Test {i+1} failed: {{e}}"
    except Exception as e:
        return False, f"Test {i+1} error: {{e}}"
"""
        
        # Create main test program
        test_program = f"""
{code}

{test_functions}

# Main execution
import sys
import json

test_results = []
passed_count = 0
failed_count = 0

# Run all tests
for i in range({len(test_cases)}):
    passed, message = locals()[f"test_{{i}}"]()
    test_results.append({{
        "test_id": i,
        "passed": passed,
        "message": message,
        "test_case": "{'Individual test'}"  # You could include the actual test case here
    }})
    if passed:
        passed_count += 1
    else:
        failed_count += 1

# Output results
output = {{
    "total_tests": {len(test_cases)},
    "passed": passed_count,
    "failed": failed_count,
    "all_passed": (failed_count == 0),
    "test_results": test_results
}}

print("JSON_RESULTS:" + json.dumps(output))

if failed_count == 0:
    print("\\nRESULT: PASSED")
    sys.exit(0)
else:
    print(f"\\nRESULT: FAILED: {{failed_count}}/{{len(test_cases)}} tests failed")
    sys.exit(1)
"""
        
        return test_program
    
    def _execute_with_docker_individual_tests(self, code: str, tests: str, problem_id: str) -> Dict:
        """Execute with Docker, running tests individually"""
        result_queue = queue.Queue()
        
        def _run_container():
            temp_file = None
            try:
                # Extract function name
                function_name = self._extract_function_name(code)
                logger.info(f"Testing function: {function_name}")
                
                # Create test program with individual tests
                test_program = self._create_individual_test_program(code, tests, function_name)
                
                # Write to temporary file
                with tempfile.NamedTemporaryFile(
                    mode="w", 
                    suffix=".py", 
                    encoding='utf-8',
                    delete=False
                ) as f:
                    f.write(test_program)
                    temp_file = f.name
                    logger.debug(f"Created temp file: {temp_file}")

                # Run in container
                logger.info(f"Starting Docker container for {problem_id}")
                output_bytes = self.client.containers.run(
                    "python:3.9-slim",
                    ["python", "/tmp/test.py"],
                    volumes={temp_file: {"bind": "/tmp/test.py", "mode": "ro"}},
                    working_dir="/tmp",
                    stderr=True,
                    stdout=True,
                    remove=True,
                    mem_limit="512m",
                )

                output = output_bytes.decode("utf-8", errors='replace') if output_bytes else ""
                logger.debug(f"Docker output (first 500 chars): {output[:500]}")
                
                # Parse JSON results from output
                test_results = []
                total_tests = 0
                passed_tests = 0
                failed_tests = 0
                all_passed = False
                
                # Look for JSON_RESULTS in output
                json_match = re.search(r'JSON_RESULTS:(\{.*?\})(?=\n|$)', output, re.DOTALL)
                if json_match:
                    try:
                        json_str = json_match.group(1)
                        result_data = json.loads(json_str)
                        test_results = result_data.get('test_results', [])
                        total_tests = result_data.get('total_tests', 0)
                        passed_tests = result_data.get('passed', 0)
                        failed_tests = result_data.get('failed', 0)
                        all_passed = result_data.get('all_passed', False)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse JSON results: {e}")
                
                # Determine overall result
                if "RESULT: PASSED" in output or all_passed:
                    result_type = "passed"
                    passed = True
                elif "RESULT: FAILED" in output or failed_tests > 0:
                    result_type = "failed"
                    passed = False
                else:
                    result_type = "error"
                    passed = False
                
                result_queue.put(("success", {
                    "passed": passed,
                    "result": result_type,
                    "output": output.strip(),
                    "test_results": test_results,
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests,
                    "test_cases": self._parse_test_cases(tests, function_name),
                    "source": "docker_individual_tests"
                }))
                
            except docker.errors.ContainerError as e:
                output = getattr(e, 'stderr', b'').decode('utf-8', errors='replace') or str(e)
                logger.error(f"Docker container error: {output[:200]}")
                result_queue.put(("error", {
                    "passed": False,
                    "result": "container_error",
                    "output": output,
                    "test_results": [],
                    "total_tests": 0,
                    "passed_tests": 0,
                    "failed_tests": 0,
                    "test_cases": [],
                    "source": "docker_error"
                }))
            except Exception as e:
                logger.error(f"Docker execution failed: {e}")
                result_queue.put(("error", {
                    "passed": False,
                    "result": f"docker_error: {e}",
                    "output": str(e),
                    "test_results": [],
                    "total_tests": 0,
                    "passed_tests": 0,
                    "failed_tests": 0,
                    "test_cases": [],
                    "source": "docker_error"
                }))
            finally:
                if temp_file and os.path.exists(temp_file):
                    try:
                        os.unlink(temp_file)
                    except Exception as e:
                        logger.warning(f"Could not delete temp file: {e}")
        
        # Run in thread with timeout
        thread = threading.Thread(target=_run_container)
        thread.daemon = True
        thread.start()
        thread.join(timeout=self.timeout)
        
        if thread.is_alive():
            return {
                "passed": False,
                "result": "timeout",
                "output": f"Execution timed out after {self.timeout} seconds",
                "test_results": [],
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "test_cases": [],
                "source": "docker_timeout"
            }
        
        if result_queue.empty():
            return {
                "passed": False,
                "result": "unknown_error",
                "output": "No result from container execution",
                "test_results": [],
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "test_cases": [],
                "source": "docker_error"
            }
        
        result_type, result = result_queue.get()
        return result
    
    def _execute_with_fallback(self, code: str, tests: str, problem_id: str) -> Dict:
        """Fallback execution without Docker"""
        try:
            logger.info(f"Using fallback execution for {problem_id}")
            
            # Extract function name
            function_name = self._extract_function_name(code)
            
            # Parse test cases
            test_cases = self._parse_test_cases(tests, function_name)
            test_results = []
            passed_count = 0
            
            # Execute the solution code
            exec_globals = {}
            exec(code, exec_globals)
            
            if test_cases:
                # Run individual test cases
                for i, test_case in enumerate(test_cases):
                    try:
                        # Create a new namespace for each test
                        test_namespace = {}
                        test_namespace.update(exec_globals)
                        
                        # Execute the test
                        exec(test_case, test_namespace)
                        test_results.append({
                            "test_id": i,
                            "passed": True,
                            "message": f"Test {i+1} passed",
                            "test_case": test_case[:100] + "..." if len(test_case) > 100 else test_case
                        })
                        passed_count += 1
                    except AssertionError as e:
                        test_results.append({
                            "test_id": i,
                            "passed": False,
                            "message": f"Test {i+1} failed: {e}",
                            "test_case": test_case[:100] + "..." if len(test_case) > 100 else test_case
                        })
                    except Exception as e:
                        test_results.append({
                            "test_id": i,
                            "passed": False,
                            "message": f"Test {i+1} error: {e}",
                            "test_case": test_case[:100] + "..." if len(test_case) > 100 else test_case
                        })
                
                all_passed = (passed_count == len(test_cases))
                
                return {
                    "passed": all_passed,
                    "result": "passed" if all_passed else "failed",
                    "output": f"Fallback execution: {passed_count}/{len(test_cases)} tests passed",
                    "test_results": test_results,
                    "total_tests": len(test_cases),
                    "passed_tests": passed_count,
                    "failed_tests": len(test_cases) - passed_count,
                    "test_cases": test_cases,
                    "source": "fallback_individual"
                }
            else:
                # Original fallback execution
                test_code = f"""
{tests}

try:
    check({function_name})
    result = "passed"
except AssertionError as e:
    result = f"failed: {{e}}"
except Exception as e:
    result = f"error: {{e}}"
"""
                
                test_globals = {}
                test_globals.update(exec_globals)
                exec(test_code, test_globals)
                result = test_globals.get("result", "unknown")
                
                return {
                    "passed": result.startswith("passed"),
                    "result": result,
                    "output": f"Fallback execution: {result}",
                    "test_results": [],
                    "total_tests": 1,
                    "passed_tests": 1 if result.startswith("passed") else 0,
                    "failed_tests": 0 if result.startswith("passed") else 1,
                    "test_cases": [],
                    "source": "fallback"
                }
                
        except Exception as e:
            logger.error(f"Fallback execution failed: {e}")
            return {
                "passed": False,
                "result": f"fallback_error: {e}",
                "output": str(e),
                "test_results": [],
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "test_cases": [],
                "source": "fallback_error"
            }

    def test_docker_connection(self) -> bool:
        """Test if Docker is working properly"""
        try:
            if not self.client:
                return False
            
            output = self.client.containers.run(
                "python:3.9-slim",
                ["python", "-c", "print('DOCKER_TEST: OK')"],
                remove=True,
                stdout=True
            )
            
            return b"DOCKER_TEST: OK" in output
                
        except Exception as e:
            logger.error(f"Docker test failed: {e}")
            return False