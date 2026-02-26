"""Test suite for managers."""
import unittest
from unittest.mock import Mock, patch, MagicMock

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.managers import EvaluationManager, ResultAggregator


class TestEvaluationManager(unittest.TestCase):
    """Test cases for EvaluationManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = EvaluationManager()
    
    def test_manager_creation(self):
        """Test creating an evaluation manager."""
        self.assertIsNotNone(self.manager)
    
    def test_run_evaluation_integration(self):
        """Test running an evaluation."""
        mock_loader = Mock()
        mock_loader.load.return_value = []
        mock_adapter = Mock()
        mock_adapter.generate.return_value = 'test_output'
        
        # This would run the actual evaluation
        result = self.manager.run_evaluation(mock_loader, mock_adapter)
        self.assertIsNotNone(result)
    
    def test_evaluation_with_timeout(self):
        """Test evaluation handles timeouts."""
        mock_loader = Mock()
        mock_adapter = Mock()
        
        # Set timeout
        results = self.manager.run_evaluation(
            mock_loader, 
            mock_adapter,
            timeout=5
        )
        self.assertIsNotNone(results)


class TestResultAggregator(unittest.TestCase):
    """Test cases for ResultAggregator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.aggregator = ResultAggregator()
    
    def test_aggregator_creation(self):
        """Test creating a result aggregator."""
        self.assertIsNotNone(self.aggregator)
    
    def test_aggregate_results(self):
        """Test aggregating results."""
        mock_results = [
            {'status': 'passed', 'time': 1.5},
            {'status': 'passed', 'time': 2.0},
            {'status': 'failed', 'time': 0.5}
        ]
        
        aggregated = self.aggregator.aggregate(mock_results)
        self.assertIsNotNone(aggregated)
        self.assertIn('pass_rate', str(aggregated).lower() or 'pass' in aggregated)
    
    def test_calculate_statistics(self):
        """Test calculating statistics."""
        mock_results = [
            {'metric': 0.8},
            {'metric': 0.9},
            {'metric': 0.7}
        ]
        
        stats = self.aggregator.calculate_statistics(mock_results)
        self.assertIsNotNone(stats)


if __name__ == '__main__':
    unittest.main()