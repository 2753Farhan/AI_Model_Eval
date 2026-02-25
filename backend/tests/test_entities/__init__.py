"""Test suite for entities."""
import unittest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Import entities
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.entities import User, Evaluation, Problem, EvaluationResult, Metric, Error, Report, Benchmark


class TestUser(unittest.TestCase):
    """Test cases for User entity."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user_data = {
            'username': 'test_user',
            'email': 'test@example.com'
        }
    
    def test_user_creation(self):
        """Test creating a user."""
        user = User(**self.user_data)
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'test@example.com')
    
    def test_user_password_hashing(self):
        """Test user password hashing."""
        user = User(username='test', email='test@example.com', password='secret123')
        self.assertIsNotNone(user.get_password_hash())


class TestEvaluation(unittest.TestCase):
    """Test cases for Evaluation entity."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.eval_data = {
            'name': 'Test Evaluation',
            'model': 'test-model'
        }
    
    def test_evaluation_creation(self):
        """Test creating an evaluation."""
        evaluation = Evaluation(**self.eval_data)
        self.assertEqual(evaluation.name, 'Test Evaluation')
        self.assertEqual(evaluation.model, 'test-model')


class TestProblem(unittest.TestCase):
    """Test cases for Problem entity."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.problem_data = {
            'title': 'Test Problem',
            'description': 'A test problem',
            'input_spec': 'int -> int',
            'output_spec': 'int'
        }
    
    def test_problem_creation(self):
        """Test creating a problem."""
        problem = Problem(**self.problem_data)
        self.assertEqual(problem.title, 'Test Problem')
        self.assertEqual(problem.description, 'A test problem')


class TestEvaluationResult(unittest.TestCase):
    """Test cases for EvaluationResult entity."""
    
    def test_result_creation(self):
        """Test creating an evaluation result."""
        result = EvaluationResult(
            problem_id='p1',
            solution='test_code',
            status='passed'
        )
        self.assertEqual(result.problem_id, 'p1')
        self.assertEqual(result.status, 'passed')


class TestMetric(unittest.TestCase):
    """Test cases for Metric entity."""
    
    def test_metric_creation(self):
        """Test creating a metric."""
        metric = Metric(name='pass_rate', value=0.85)
        self.assertEqual(metric.name, 'pass_rate')
        self.assertEqual(metric.value, 0.85)


class TestError(unittest.TestCase):
    """Test cases for Error entity."""
    
    def test_error_creation(self):
        """Test creating an error."""
        error = Error(
            type='SyntaxError',
            message='Invalid syntax',
            traceback='...'
        )
        self.assertEqual(error.type, 'SyntaxError')
        self.assertEqual(error.message, 'Invalid syntax')


class TestReport(unittest.TestCase):
    """Test cases for Report entity."""
    
    def test_report_creation(self):
        """Test creating a report."""
        report = Report(
            title='Evaluation Report',
            evaluation_id='eval1'
        )
        self.assertEqual(report.title, 'Evaluation Report')
        self.assertEqual(report.evaluation_id, 'eval1')


class TestBenchmark(unittest.TestCase):
    """Test cases for Benchmark entity."""
    
    def test_benchmark_creation(self):
        """Test creating a benchmark."""
        benchmark = Benchmark(
            name='HumanEval',
            description='HumanEval benchmark'
        )
        self.assertEqual(benchmark.name, 'HumanEval')


if __name__ == '__main__':
    unittest.main()