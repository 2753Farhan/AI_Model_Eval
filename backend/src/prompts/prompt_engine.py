from typing import Dict, Any, Optional, List
import logging
from pathlib import Path
import json

from .strategies import PromptStrategy, ZeroShotStrategy, FewShotStrategy, ChainOfThoughtStrategy

logger = logging.getLogger(__name__)


class PromptEngine:
    """Engine for managing prompt strategies"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.strategies: Dict[str, PromptStrategy] = {}
        self.default_strategy = config.get('default_strategy', 'zero_shot')
        
        # Load examples first
        self.examples = self._load_examples()
        
        # Initialize default strategies after examples are loaded
        self._register_default_strategies()
        
        logger.info(f"PromptEngine initialized with {len(self.strategies)} strategies")

    def _register_default_strategies(self):
        """Register default prompt strategies"""
        self.register_strategy('zero_shot', ZeroShotStrategy())
        self.register_strategy('few_shot', FewShotStrategy(self.examples))
        self.register_strategy('chain_of_thought', ChainOfThoughtStrategy())

    def register_strategy(self, name: str, strategy: PromptStrategy) -> None:
        """Register a new prompt strategy"""
        self.strategies[name] = strategy
        logger.debug(f"Registered strategy: {name}")

    def format_prompt(
        self,
        problem: Dict[str, Any],
        strategy: str = 'zero_shot',
        **kwargs
    ) -> str:
        """Format prompt using specified strategy"""
        if strategy not in self.strategies:
            logger.warning(f"Strategy {strategy} not found, using {self.default_strategy}")
            strategy = self.default_strategy
        
        prompt_strategy = self.strategies[strategy]
        return prompt_strategy.format(problem, **kwargs)

    def get_available_strategies(self) -> List[str]:
        """Get list of available strategies"""
        return list(self.strategies.keys())

    def _load_examples(self) -> List[Dict[str, str]]:
        """Load examples for few-shot learning"""
        examples = []
        
        # Default examples
        default_examples = [
            {
                'problem': 'Write a function to add two numbers',
                'solution': '''
def add(a, b):
    """Add two numbers and return the result."""
    return a + b
'''
            },
            {
                'problem': 'Write a function to check if a number is even',
                'solution': '''
def is_even(n):
    """Check if a number is even."""
    return n % 2 == 0
'''
            },
            {
                'problem': 'Write a function to find the maximum of three numbers',
                'solution': '''
def max_of_three(a, b, c):
    """Find the maximum of three numbers."""
    return max(a, b, c)
'''
            }
        ]
        
        examples.extend(default_examples)
        
        # Load custom examples from file if exists
        examples_file = self.config.get('examples_file')
        if examples_file and Path(examples_file).exists():
            try:
                with open(examples_file, 'r') as f:
                    custom_examples = json.load(f)
                    examples.extend(custom_examples)
            except Exception as e:
                logger.error(f"Failed to load examples file: {e}")
        
        return examples