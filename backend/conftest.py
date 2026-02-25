"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import pytest


@pytest.fixture
def temp_dir(tmp_path):
    """Fixture providing a temporary directory."""
    return tmp_path


@pytest.fixture
def mock_config():
    """Fixture providing a mock configuration."""
    return {
        'models': ['test-model'],
        'timeout': 30,
        'memory_limit': '4GB'
    }


@pytest.fixture
def sample_problem():
    """Fixture providing a sample problem."""
    return {
        'id': 'test_1',
        'title': 'Test Problem',
        'description': 'A test problem',
        'input_spec': 'int -> int',
        'output_spec': 'int',
        'test_cases': [
            {'input': '5', 'output': '25'}
        ]
    }


@pytest.fixture
def sample_solution():
    """Fixture providing a sample solution."""
    return '''def solution(x):
    return x * x
'''
