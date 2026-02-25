"""Test suite for adapters."""
import unittest
from unittest.mock import Mock, patch, MagicMock

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.adapters import ModelAdapter, ModelRegistry


class TestModelAdapter(unittest.TestCase):
    """Test cases for ModelAdapter abstract class."""
    
    def test_adapter_is_abstract(self):
        """Test that ModelAdapter cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            ModelAdapter()
    
    def test_adapter_requires_load_model(self):
        """Test that subclasses must implement load_model."""
        class IncompleteAdapter(ModelAdapter):
            def generate(self, prompt):
                pass
        
        with self.assertRaises(TypeError):
            IncompleteAdapter()
    
    def test_adapter_requires_generate(self):
        """Test that subclasses must implement generate."""
        class IncompleteAdapter(ModelAdapter):
            def load_model(self):
                pass
        
        with self.assertRaises(TypeError):
            IncompleteAdapter()


class TestModelRegistry(unittest.TestCase):
    """Test cases for ModelRegistry."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = ModelRegistry()
    
    def test_registry_creation(self):
        """Test creating a model registry."""
        self.assertIsNotNone(self.registry)
    
    def test_register_adapter(self):
        """Test registering an adapter."""
        mock_adapter_class = Mock()
        self.registry.register('test_model', mock_adapter_class)
        
        retrieved = self.registry.get('test_model')
        self.assertEqual(retrieved, mock_adapter_class)
    
    def test_get_nonexistent_adapter(self):
        """Test getting a non-existent adapter."""
        result = self.registry.get('nonexistent')
        self.assertIsNone(result)
    
    def test_multiple_adapters(self):
        """Test registering multiple adapters."""
        mock_adapter1 = Mock()
        mock_adapter2 = Mock()
        
        self.registry.register('model1', mock_adapter1)
        self.registry.register('model2', mock_adapter2)
        
        self.assertEqual(self.registry.get('model1'), mock_adapter1)
        self.assertEqual(self.registry.get('model2'), mock_adapter2)


if __name__ == '__main__':
    unittest.main()