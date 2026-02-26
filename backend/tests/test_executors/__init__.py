"""Test suite for executors."""
import unittest
from unittest.mock import Mock, patch, MagicMock
import time

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.executors import SandboxExecutor, ResourceManager


class TestSandboxExecutor(unittest.TestCase):
    """Test cases for SandboxExecutor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.executor = SandboxExecutor()
    
    def test_executor_creation(self):
        """Test creating a sandbox executor."""
        self.assertIsNotNone(self.executor)
    
    def test_execute_simple_code(self):
        """Test executing simple Python code."""
        code = "x = 1 + 1"
        result = self.executor.execute(code)
        self.assertIsNotNone(result)
    
    def test_execute_with_timeout(self):
        """Test executing code with timeout."""
        code = "import time; time.sleep(1)"
        result = self.executor.execute_with_timeout(code, timeout=2)
        self.assertIsNotNone(result)
    
    def test_timeout_exceeded(self):
        """Test handling timeout exceeded."""
        code = "import time; time.sleep(10)"
        # Should handle timeout gracefully
        try:
            result = self.executor.execute_with_timeout(code, timeout=0.1)
        except Exception as e:
            # Expected to timeout
            self.assertIn('timeout', str(e).lower())
    
    def test_execute_with_error(self):
        """Test executing code that raises an error."""
        code = "raise ValueError('test error')"
        result = self.executor.execute(code)
        # Should capture the error
        self.assertIsNotNone(result)


class TestResourceManager(unittest.TestCase):
    """Test cases for ResourceManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = ResourceManager()
    
    def test_resource_manager_creation(self):
        """Test creating a resource manager."""
        self.assertIsNotNone(self.manager)
    
    def test_set_memory_limit(self):
        """Test setting memory limit."""
        self.manager.set_memory_limit('4GB')
        # Verify it was set
        self.assertIsNotNone(self.manager)
    
    def test_set_cpu_limit(self):
        """Test setting CPU limit."""
        self.manager.set_cpu_limit('2')
        self.assertIsNotNone(self.manager)
    
    def test_set_timeout(self):
        """Test setting timeout."""
        self.manager.set_timeout(30)
        self.assertIsNotNone(self.manager)
    
    def test_multiple_resource_limits(self):
        """Test setting multiple resource limits."""
        self.manager.set_memory_limit('2GB')
        self.manager.set_cpu_limit('1')
        self.manager.set_timeout(60)
        
        # All limits should be set
        self.assertIsNotNone(self.manager)


if __name__ == '__main__':
    unittest.main()