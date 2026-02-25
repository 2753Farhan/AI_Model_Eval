"""Tests package."""
import unittest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def discover_tests():
    """Discover and return all tests in the tests package."""
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    return suite


def run_all_tests():
    """Run all tests in the package."""
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(discover_tests())


if __name__ == '__main__':
    run_all_tests()