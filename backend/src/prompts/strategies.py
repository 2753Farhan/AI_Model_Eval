
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import textwrap


class PromptStrategy(ABC):
    """Abstract base class for prompt strategies"""
    
    @abstractmethod
    def format(self, problem: Dict[str, Any], **kwargs) -> str:
        """Format the prompt"""
        pass


class ZeroShotStrategy(PromptStrategy):
    """Zero-shot prompting strategy"""
    
    def format(self, problem: Dict[str, Any], **kwargs) -> str:
        prompt = problem.get('prompt', '')
        
        # Add any additional context
        if 'context' in kwargs:
            prompt = f"{kwargs['context']}\n\n{prompt}"
        
        # Add instructions
        prompt += "\n\n# Complete the function below:\n"
        
        # Add function signature if available
        if 'function_signature' in problem:
            prompt += f"\n{problem['function_signature']}\n"
        
        return prompt


class FewShotStrategy(PromptStrategy):
    """Few-shot prompting strategy with examples"""
    
    def __init__(self, examples: List[Dict[str, str]]):
        self.examples = examples
    
    def format(self, problem: Dict[str, Any], **kwargs) -> str:
        # Use provided examples or default ones
        examples = kwargs.get('examples', self.examples)
        num_examples = kwargs.get('num_examples', 2)
        
        # Format examples
        examples_text = ""
        for i, example in enumerate(examples[:num_examples]):
            examples_text += f"""
Example {i + 1}:
Problem: {example['problem']}
Solution:
{textwrap.dedent(example['solution']).strip()}

"""
        
        # Add current problem
        prompt = f"""{examples_text}
Now solve this problem:

{problem.get('prompt', '')}

# Complete the function below:
"""
        
        # Add function signature if available
        if 'function_signature' in problem:
            prompt += f"\n{problem['function_signature']}\n"
        
        return prompt


class ChainOfThoughtStrategy(PromptStrategy):
    """Chain-of-thought prompting strategy"""
    
    def format(self, problem: Dict[str, Any], **kwargs) -> str:
        prompt = f"""{problem.get('prompt', '')}

# Let's think through this step by step:

# Step 1: Understand the problem requirements
- What inputs does the function need?
- What output should it produce?
- Are there any edge cases to consider?

# Step 2: Plan the approach
- What algorithm or method should we use?
- What are the key steps in the solution?

# Step 3: Write the solution
"""
        
        # Add function signature if available
        if 'function_signature' in problem:
            prompt += f"\n{problem['function_signature']}\n"
        
        return prompt


class InstructionStrategy(PromptStrategy):
    """Instruction-based prompting with detailed guidelines"""
    
    def format(self, problem: Dict[str, Any], **kwargs) -> str:
        instructions = kwargs.get('instructions', """
Follow these guidelines when writing the solution:
1. Write clean, readable code with appropriate comments
2. Handle edge cases (empty input, invalid values)
3. Use descriptive variable names
4. Follow PEP 8 style guidelines
5. Include docstrings for the function
""")
        
        prompt = f"""{instructions}

Now solve this problem:

{problem.get('prompt', '')}

# Complete the function below:
"""
        
        # Add function signature if available
        if 'function_signature' in problem:
            prompt += f"\n{problem['function_signature']}\n"
        
        return prompt


class CodeReviewStrategy(PromptStrategy):
    """Strategy that asks the model to review and improve its own code"""
    
    def format(self, problem: Dict[str, Any], **kwargs) -> str:
        prompt = f"""{problem.get('prompt', '')}

# First, write a solution to this problem:

"""
        
        # Add function signature if available
        if 'function_signature' in problem:
            prompt += f"\n{problem['function_signature']}\n"
        
        prompt += """
# Now, review your solution and identify any issues:
# - Are there any edge cases not handled?
# - Is the code efficient?
# - Is it readable and well-documented?

# Finally, provide an improved version of the solution:
"""
        
        return prompt