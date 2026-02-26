"""AI Model Evaluation Framework.

A comprehensive framework for evaluating AI models on various benchmarks and datasets.
"""

__version__ = '1.0.0'
__author__ = 'AI Evaluation Team'

from . import entities
from . import managers
from . import adapters
from . import loaders
from . import executors
from . import calculators
from . import analyzers
from . import generators
from . import prompts
from . import dashboard
from . import utils
from . import config

__all__ = [
    'entities',
    'managers',
    'adapters',
    'loaders',
    'executors',
    'calculators',
    'analyzers',
    'generators',
    'prompts',
    'dashboard',
    'utils',
    'config',
]
