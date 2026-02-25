# src/executors/sandbox_executor.py

from typing import List, Dict, Any, Optional, Callable
import asyncio
import docker
import tempfile
import os
import signal
import threading
import queue
import json
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class SandboxExecutor:
    """Safe code execution in Docker sandbox"""
    
    def __init__(
        self,
        timeout: int = 30,
        memory_limit: str = "512m",
        cpu_limit: float = 1.0,
        network_enabled: bool = False,
        docker_client: Optional[docker.DockerClient] = None
    ):
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self.network_enabled = network_enabled
        self.docker_client = docker_client or self._init_docker()
        self.temp_dir = tempfile.mkdtemp(prefix="sandbox_")
        self.supported_languages = self._detect_supported_languages()
        
        logger.info(f"SandboxExecutor initialized with timeout={timeout}s, memory={memory_limit}")

    def _init_docker(self) -> Optional[docker.DockerClient]:
        """Initialize Docker client"""
        try:
            client = docker.from_env()
            # Test connection
            client.ping()
            logger.info("Docker client initialized successfully")
            return client
        except Exception as e:
            logger.warning(f"Docker not available: {e}. Using fallback execution.")
            return None

    def _detect_supported_languages(self) -> List[str]:
        """Detect supported languages"""
        languages = ['python']
        
        if self.docker_client:
            # Check if we have images for other languages
            try:
                images = self.docker_client.images.list()
                image_tags = []
                for img in images:
                    image_tags.extend(img.tags)
                
                language_images = {
                    'python': ['python:3.9-slim', 'python:3.8-slim'],
                    'javascript': ['node:16-slim'],
                    'java': ['openjdk:11-slim'],
                    'cpp': ['gcc:latest'],
                    'go': ['golang:1.17']
                }
                
                for lang, required_images in language_images.items():
                    if any(any(req in tag for req in required_images) for tag in image_tags):
                        languages.append(lang)
            except Exception as e:
                logger.warning(f"Failed to detect language images: {e}")
        
        return languages

    async def execute_safely(
        self,
        code: str,
        test_cases: List[Dict[str, Any]],
        problem_id: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """Execute code safely"""
        if language not in self.supported_languages:
            return {
                'passed': False,
                'result': 'unsupported_language',
                'output': f"Language {language} not supported",
                'test_results': [],
                'errors': [{
                    'error_type': 'unsupported_language',
                    'error_message': f"Language {language} not supported"
                }],
                'execution_time_ms': 0
            }

        if self.docker_client:
            return await self._execute_with_docker(code, test_cases, problem_id, language)
        else:
            return await self._execute_with_fallback(code, test_cases, language)

    async def _execute_with_docker(
        self,
        code: str,
        test_cases: List[Dict[str, Any]],
        problem_id: str,
        language: str
    ) -> Dict[str, Any]:
        """Execute with Docker sandbox"""
        result_queue = queue.Queue()
        start_time = time.time()
        
        def run_container():
            temp_file = None
            try:
                # Create test program
                test_program = self._create_test_program(code, test_cases, language)
                
                # Write to temp file
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    suffix=self._get_file_extension(language),
                    encoding='utf-8',
                    delete=False
                ) as f:
                    f.write(test_program)
                    temp_file = f.name
                
                # Get container image
                image = self._get_language_image(language)
                
                # Run container
                container = self.docker_client.containers.run(
                    image,
                    self._get_execution_command(language, "/tmp/test"),
                    volumes={temp_file: {"bind": "/tmp/test", "mode": "ro"}},
                    working_dir="/tmp",
                    stderr=True,
                    stdout=True,
                    remove=False,
                    mem_limit=self.memory_limit,
                    nano_cpus=int(self.cpu_limit * 1e9),
                    network_disabled=not self.network_enabled,
                    detach=True
                )
                
                # Wait for completion with timeout
                try:
                    container.wait(timeout=self.timeout)
                    logs = container.logs(stdout=True, stderr=True).decode('utf-8', errors='replace')
                    
                    # Parse results
                    execution_result = self._parse_execution_output(logs)
                    
                except docker.errors.APIError as e:
                    if "Timeout" in str(e):
                        container.kill()
                        execution_result = {
                            'passed': False,
                            'result': 'timeout',
                            'output': f"Execution timed out after {self.timeout} seconds",
                            'test_results': []
                        }
                    else:
                        raise
                
                finally:
                    container.remove()
                
                result_queue.put(execution_result)
                
            except Exception as e:
                logger.error(f"Docker execution failed: {e}")
                result_queue.put({
                    'passed': False,
                    'result': f'container_error: {str(e)}',
                    'output': str(e),
                    'test_results': []
                })
            
            finally:
                if temp_file and os.path.exists(temp_file):
                    try:
                        os.unlink(temp_file)
                    except Exception as e:
                        logger.warning(f"Could not delete temp file: {e}")
        
        # Run in thread
        thread = threading.Thread(target=run_container)
        thread.daemon = True
        thread.start()
        thread.join(timeout=self.timeout + 5)
        
        execution_time_ms = (time.time() - start_time) * 1000
        
        if thread.is_alive():
            return {
                'passed': False,
                'result': 'timeout',
                'output': f"Execution timed out after {self.timeout} seconds",
                'test_results': [],
                'execution_time_ms': execution_time_ms
            }
        
        if result_queue.empty():
            return {
                'passed': False,
                'result': 'unknown_error',
                'output': "No result from container",
                'test_results': [],
                'execution_time_ms': execution_time_ms
            }
        
        result = result_queue.get()
        result['execution_time_ms'] = execution_time_ms
        return result

    def _create_test_program(
        self,
        code: str,
        test_cases: List[Dict[str, Any]],
        language: str
    ) -> str:
        """Create a test program for the given language"""
        if language == 'python':
            return self._create_python_test_program(code, test_cases)
        elif language == 'javascript':
            return self._create_javascript_test_program(code, test_cases)
        elif language == 'java':
            return self._create_java_test_program(code, test_cases)
        else:
            return code

    def _create_python_test_program(self, code: str, test_cases: List[Dict]) -> str:
        """Create Python test program"""
        test_functions = ""
        for i, test in enumerate(test_cases):
            if 'assertion' in test:
                test_functions += f"""
def test_{i}():
    try:
        {test['assertion']}
        return True, "Test {i+1} passed"
    except AssertionError as e:
        return False, f"Test {i+1} failed: {{e}}"
    except Exception as e:
        return False, f"Test {i+1} error: {{e}}"
"""
        
        return f"""
{code}

{test_functions}

import json
import sys

test_results = []
passed_count = 0
failed_count = 0

# Get all test functions dynamically
for i in range({len(test_cases)}):
    func_name = f"test_{{i}}"
    if func_name in locals():
        passed, message = locals()[func_name]()
        test_results.append({{
            "test_id": i,
            "passed": passed,
            "message": message,
            "test_case": {json.dumps(test_cases[i] if i < len(test_cases) else {})}
        }})
        if passed:
            passed_count += 1
        else:
            failed_count += 1

output = {{
    "total_tests": {len(test_cases)},
    "passed": passed_count,
    "failed": failed_count,
    "test_results": test_results
}}

print("JSON_RESULTS:" + json.dumps(output))

if failed_count == 0:
    sys.exit(0)
else:
    sys.exit(1)
"""

    def _create_javascript_test_program(self, code: str, test_cases: List[Dict]) -> str:
        """Create JavaScript test program"""
        test_code = ""
        for i, test in enumerate(test_cases):
            if 'assertion' in test:
                # Convert Python assertion to JS-style test
                test_code += f"""
function test_{i}() {{
    try {{
        {test['assertion'].replace('assert', 'console.assert')};
        return {{passed: true, message: "Test {i+1} passed"}};
    }} catch(e) {{
        return {{passed: false, message: "Test {i+1} failed: " + e.message}};
    }}
}}
"""
        
        return f"""
{code}

{test_code}

const test_results = [];
let passed_count = 0;
let failed_count = 0;

for (let i = 0; i < {len(test_cases)}; i++) {{
    const test_func = eval(`test_${{i}}`);
    if (test_func) {{
        const result = test_func();
        test_results.push({{
            test_id: i,
            passed: result.passed,
            message: result.message,
            test_case: {json.dumps(test_cases)}
        }});
        if (result.passed) passed_count++;
        else failed_count++;
    }}
}}

const output = {{
    total_tests: {len(test_cases)},
    passed: passed_count,
    failed: failed_count,
    test_results: test_results
}};

console.log("JSON_RESULTS:" + JSON.stringify(output));
process.exit(failed_count === 0 ? 0 : 1);
"""

    def _create_java_test_program(self, code: str, test_cases: List[Dict]) -> str:
        """Create Java test program"""
        # This is a simplified version - you'd need to parse the Java code properly
        return code

    def _parse_execution_output(self, output: str) -> Dict[str, Any]:
        """Parse execution output"""
        test_results = []
        passed = False
        result = "unknown"
        
        # Look for JSON results
        import re
        json_match = re.search(r'JSON_RESULTS:(\{.*?\})(?:\n|$)', output, re.DOTALL)
        
        if json_match:
            try:
                json_str = json_match.group(1)
                data = json.loads(json_str)
                test_results = data.get('test_results', [])
                passed = data.get('failed', 0) == 0
                result = "passed" if passed else "failed"
            except json.JSONDecodeError:
                pass
        
        # Fallback to simple parsing
        if not test_results:
            if "RESULT: PASSED" in output or "All tests passed" in output:
                passed = True
                result = "passed"
            elif "FAILED" in output or "Error" in output:
                passed = False
                result = "failed"
        
        return {
            'passed': passed,
            'result': result,
            'output': output.strip(),
            'test_results': test_results
        }

    def _get_file_extension(self, language: str) -> str:
        """Get file extension for language"""
        extensions = {
            'python': '.py',
            'javascript': '.js',
            'java': '.java',
            'cpp': '.cpp',
            'go': '.go'
        }
        return extensions.get(language, '.txt')

    def _get_language_image(self, language: str) -> str:
        """Get Docker image for language"""
        images = {
            'python': 'python:3.9-slim',
            'javascript': 'node:16-slim',
            'java': 'openjdk:11-slim',
            'cpp': 'gcc:latest',
            'go': 'golang:1.17'
        }
        return images.get(language, 'python:3.9-slim')

    def _get_execution_command(self, language: str, file_path: str) -> List[str]:
        """Get execution command for language"""
        commands = {
            'python': ['python', file_path],
            'javascript': ['node', file_path],
            'java': ['java', file_path],
            'cpp': ['sh', '-c', f'g++ {file_path}.cpp -o /tmp/a.out && /tmp/a.out'],
            'go': ['go', 'run', file_path]
        }
        return commands.get(language, ['python', file_path])

    async def _execute_with_fallback(
        self,
        code: str,
        test_cases: List[Dict[str, Any]],
        language: str
    ) -> Dict[str, Any]:
        """Fallback execution without Docker"""
        if language != 'python':
            return {
                'passed': False,
                'result': 'unsupported_language',
                'output': f"Fallback only supports Python, not {language}",
                'test_results': [],
                'errors': [{
                    'error_type': 'unsupported_language',
                    'error_message': f"Fallback only supports Python"
                }],
                'execution_time_ms': 0
            }
        
        start_time = time.time()
        test_results = []
        passed_count = 0
        
        try:
            # Create a namespace for execution
            namespace = {}
            
            # Execute the code to define the function
            exec(code, namespace)
            
            # Find the function name - look for the first function defined
            function_name = None
            for key, value in namespace.items():
                if callable(value) and not key.startswith('__'):
                    function_name = key
                    break
            
            # Run test cases
            for i, test in enumerate(test_cases):
                try:
                    if 'assertion' in test:
                        # Get the assertion string
                        assertion = test['assertion']
                        
                        # If the assertion uses 'candidate', replace it with the actual function name
                        if function_name and 'candidate' in assertion:
                            assertion = assertion.replace('candidate', function_name)
                        
                        # Execute the assertion in the namespace
                        exec(assertion, namespace)
                        test_results.append({
                            'test_id': i,
                            'passed': True,
                            'message': f"Test {i+1} passed"
                        })
                        passed_count += 1
                    else:
                        test_results.append({
                            'test_id': i,
                            'passed': False,
                            'message': f"Test {i+1} skipped: unknown format"
                        })
                except AssertionError as e:
                    test_results.append({
                        'test_id': i,
                        'passed': False,
                        'message': f"Test {i+1} failed: {str(e)}",
                        'test_case': test.get('assertion', '')
                    })
                except Exception as e:
                    test_results.append({
                        'test_id': i,
                        'passed': False,
                        'message': f"Test {i+1} error: {str(e)}",
                        'test_case': test.get('assertion', '')
                    })
            
            execution_time_ms = (time.time() - start_time) * 1000
            all_passed = passed_count == len(test_cases)
            
            return {
                'passed': all_passed,
                'result': 'passed' if all_passed else 'failed',
                'output': f"Executed {len(test_cases)} tests, {passed_count} passed",
                'test_results': test_results,
                'execution_time_ms': execution_time_ms,
                'errors': []
            }
            
        except SyntaxError as e:
            execution_time_ms = (time.time() - start_time) * 1000
            return {
                'passed': False,
                'result': f'syntax_error: {str(e)}',
                'output': str(e),
                'test_results': test_results,
                'execution_time_ms': execution_time_ms,
                'errors': [{
                    'error_type': 'syntax_error',
                    'error_message': str(e),
                    'line': getattr(e, 'lineno', None)
                }]
            }
        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            return {
                'passed': False,
                'result': f'execution_error: {str(e)}',
                'output': str(e),
                'test_results': test_results,
                'execution_time_ms': execution_time_ms,
                'errors': [{
                    'error_type': 'execution_error',
                    'error_message': str(e)
                }]
            }

    def set_resource_limits(
        self,
        timeout: Optional[int] = None,
        memory_limit: Optional[str] = None,
        cpu_limit: Optional[float] = None
    ) -> None:
        """Set resource limits"""
        if timeout is not None:
            self.timeout = timeout
        if memory_limit is not None:
            self.memory_limit = memory_limit
        if cpu_limit is not None:
            self.cpu_limit = cpu_limit
        
        logger.info(f"Updated limits: timeout={self.timeout}, memory={self.memory_limit}, cpu={self.cpu_limit}")

    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return self.supported_languages.copy()

    def cleanup(self) -> None:
        """Clean up temporary files"""
        import shutil
        if os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                logger.info(f"Cleaned up temp directory: {self.temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to clean up temp directory: {e}")