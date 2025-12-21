from typing import Dict, List
import textwrap

class PromptEngine:
    def __init__(self):
        self.strategies = {
            "zero_shot": self._zero_shot_prompt,
            "few_shot": self._few_shot_prompt,
            "chain_of_thought": self._cot_prompt
        }
    
    def _zero_shot_prompt(self, problem: Dict) -> str:
        """Basic zero-shot prompt"""
        prompt = f'''{problem["prompt"]}

# Complete the function below:
'''
        return prompt
    
    def _few_shot_prompt(self, problem: Dict) -> str:
        """Few-shot prompt with examples"""
        examples = '''
# Example 1:
# Problem: Write a function to add two numbers
# Solution:
def add(a, b):
    """Add two numbers and return the result."""
    return a + b

# Example 2:  
# Problem: Write a function to check if a number is even
# Solution:
def is_even(n):
    """Check if a number is even."""
    return n % 2 == 0

'''
        prompt = f'''{examples}
# Now solve this problem:
{problem["prompt"]}

# Complete the function below:
'''
        return prompt
    
    def _cot_prompt(self, problem: Dict) -> str:
        """Chain-of-thought prompt"""
        prompt = f'''{problem["prompt"]}

# Let's think step by step. First, understand the problem and requirements.
# Then, write the solution function:

'''
        return prompt
    
    def format_prompt(self, problem: Dict, strategy: str = "zero_shot") -> str:
        """Format prompt using specified strategy"""
        if strategy not in self.strategies:
            strategy = "zero_shot"
        
        return self.strategies[strategy](problem)
    
    def get_available_strategies(self) -> List[str]:
        """Get list of available prompt strategies"""
        return list(self.strategies.keys())