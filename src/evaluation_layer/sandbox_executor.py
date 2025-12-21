import docker
import logging
import os
import tempfile
import textwrap
import ast
import threading
import queue
from typing import Dict

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
            return self._execute_with_docker_threaded(code, tests, problem_id)
        
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
    
    def _execute_with_docker_threaded(self, code: str, tests: str, problem_id: str) -> Dict:
        """Execute using a Docker container with thread-based timeout"""
        result_queue = queue.Queue()
        
        def _run_container():
            temp_file = None
            try:
                # Extract the actual function name from the generated code
                function_name = self._extract_function_name(code)
                logger.info(f"Using function name '{function_name}' for test execution")
                
                # Create complete test program with proper function name
                test_program = f"""
{code}

{tests}

# Run the test
import sys
try:
    check({function_name})
    print("RESULT: PASSED")
    sys.exit(0)
except AssertionError as e:
    print(f"RESULT: FAILED: {{e}}")
    sys.exit(1)
except Exception as e:
    print(f"RESULT: ERROR: {{e}}")
    sys.exit(2)
"""

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

                # Run in container WITHOUT timeout parameter
                logger.info(f"Starting Docker container execution for {problem_id}")
                output_bytes = self.client.containers.run(
                    "python:3.9-slim",
                    ["python", "/tmp/test.py"],
                    volumes={temp_file: {"bind": "/tmp/test.py", "mode": "ro"}},
                    working_dir="/tmp",
                    stderr=True,
                    stdout=True,
                    remove=True,
                    mem_limit="512m",  # Limit container memory usage
                )

                output = output_bytes.decode("utf-8", errors='replace') if output_bytes else ""
                logger.debug(f"Docker output: {output[:200]}...")
                
                passed = "RESULT: PASSED" in output
                result_type = "passed" if passed else ("failed" if "RESULT: FAILED" in output else "error")
                
                result_queue.put(("success", {
                    "passed": passed,
                    "result": result_type,
                    "output": output.strip(),
                    "source": "docker"
                }))
                
            except docker.errors.ContainerError as e:
                # Container exited with non-zero status
                output = getattr(e, 'stderr', b'').decode('utf-8', errors='replace') or str(e)
                logger.error(f"Docker container error: {output[:200]}")
                result_queue.put(("error", {
                    "passed": False,
                    "result": "container_error",
                    "output": output,
                    "source": "docker_error"
                }))
            except Exception as e:
                logger.error(f"Docker execution failed: {e}")
                result_queue.put(("error", {
                    "passed": False,
                    "result": f"docker_error: {e}",
                    "output": str(e),
                    "source": "docker_error"
                }))
            finally:
                if temp_file and os.path.exists(temp_file):
                    try:
                        os.unlink(temp_file)
                        logger.debug(f"Cleaned up temp file: {temp_file}")
                    except Exception as e:
                        logger.warning(f"Could not delete temp file {temp_file}: {e}")
        
        # Run container in thread with timeout
        thread = threading.Thread(target=_run_container)
        thread.daemon = True
        thread.start()
        thread.join(timeout=self.timeout)
        
        if thread.is_alive():
            # Timeout occurred
            logger.warning(f"Container execution timed out after {self.timeout}s")
            return {
                "passed": False,
                "result": "timeout",
                "output": f"Execution timed out after {self.timeout} seconds",
                "source": "docker_timeout"
            }
        
        # Get result from queue
        if result_queue.empty():
            logger.error("No result from container execution")
            return {
                "passed": False,
                "result": "unknown_error",
                "output": "No result from container execution",
                "source": "docker_error"
            }
        
        result_type, result = result_queue.get()
        return result
    
    def _execute_with_fallback(self, code: str, tests: str, problem_id: str) -> Dict:
        """Fallback execution without Docker (less safe)"""
        try:
            logger.info(f"Using fallback execution for {problem_id}")
            
            # Extract function name
            function_name = self._extract_function_name(code)
            logger.info(f"Fallback using function name: {function_name}")
            
            # Execute the solution code
            exec_globals = {}
            exec(code, exec_globals)
            
            # Prepare test execution with proper function name
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
            
            # Create separate namespace for test execution
            test_globals = {}
            test_globals.update(exec_globals)  # Include the function
            
            # Execute the test code
            exec(test_code, test_globals)
            
            result = test_globals.get("result", "unknown")
            
            return {
                "passed": result.startswith("passed"),
                "result": result,
                "output": f"Fallback execution: {result}",
                "source": "fallback"
            }
            
        except Exception as e:
            logger.error(f"Fallback execution failed: {e}")
            return {
                "passed": False,
                "result": f"fallback_error: {e}",
                "output": str(e),
                "source": "fallback_error"
            }

    def test_docker_connection(self) -> bool:
        """Test if Docker is working properly"""
        try:
            if not self.client:
                logger.warning("Docker client not initialized")
                return False
            
            # Test with a simple container WITHOUT timeout parameter
            output = self.client.containers.run(
                "python:3.9-slim",
                ["python", "-c", "print('DOCKER_TEST: OK')"],
                remove=True,
                stdout=True,
                stderr=True
            )
            
            if b"DOCKER_TEST: OK" in output:
                logger.info("Docker connection test passed")
                return True
            else:
                logger.warning(f"Docker test unexpected output: {output}")
                return False
                
        except Exception as e:
            logger.error(f"Docker connection test failed: {e}")
            return False