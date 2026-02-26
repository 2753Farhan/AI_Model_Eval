"""
Example usage of the AI Model Evaluation Framework.
"""

from src.entities import User, Evaluation, Problem
from src.managers import EvaluationManager
from src.adapters import ModelRegistry, OllamaAdapter, HuggingFaceAdapter
from src.loaders import HumanEvalLoader
from src.generators import ReportGenerator
from src.prompts import PromptEngine
from src.config import config


def example_basic_usage():
    """Example: Basic framework usage."""
    print("=" * 50)
    print("Example 1: Basic Usage")
    print("=" * 50)
    
    # Create a user
    user = User(username='demo_user', email='demo@example.com')
    print(f"Created user: {user.username}")
    
    # Create an evaluation
    evaluation = Evaluation(name='Demo Evaluation', model='demo-model')
    print(f"Created evaluation: {evaluation.name}")
    
    # Create a problem
    problem = Problem(
        title='Hello World',
        description='Write a function that returns "Hello World"',
        input_spec='None',
        output_spec='str'
    )
    print(f"Created problem: {problem.title}")


def example_model_registry():
    """Example: Using model registry."""
    print("\n" + "=" * 50)
    print("Example 2: Model Registry")
    print("=" * 50)
    
    # Create registry and register adapters
    registry = ModelRegistry()
    registry.register('ollama', OllamaAdapter)
    registry.register('huggingface', HuggingFaceAdapter)
    
    print("Registered adapters:")
    for name in ['ollama', 'huggingface']:
        adapter = registry.get(name)
        print(f"  - {name}: {adapter.__name__ if adapter else 'Not found'}")


def example_configuration():
    """Example: Configuration management."""
    print("\n" + "=" * 50)
    print("Example 3: Configuration Management")
    print("=" * 50)
    
    # Access configuration
    timeout = config.get('evaluation.timeout', 30)
    memory = config.get('evaluation.memory_limit', '4GB')
    
    print(f"Evaluation timeout: {timeout}s")
    print(f"Memory limit: {memory}")
    
    # Set configuration
    config.set('evaluation.timeout', 60)
    print(f"Updated timeout: {config.get('evaluation.timeout')}")


def example_evaluation_flow():
    """Example: Complete evaluation flow."""
    print("\n" + "=" * 50)
    print("Example 4: Evaluation Flow (Simplified)")
    print("=" * 50)
    
    # Initialize components
    manager = EvaluationManager()
    loader = HumanEvalLoader()
    registry = ModelRegistry()
    
    print("Initialized evaluation components:")
    print("  - EvaluationManager")
    print("  - HumanEvalLoader")
    print("  - ModelRegistry")
    
    # In a real scenario, you would:
    # 1. Load dataset
    # 2. Register models
    # 3. Run evaluations
    # 4. Aggregate results
    # 5. Generate reports


def example_prompting():
    """Example: Prompt strategies."""
    print("\n" + "=" * 50)
    print("Example 5: Prompt Strategies")
    print("=" * 50)
    
    engine = PromptEngine()
    
    problem = {
        'title': 'Sum two numbers',
        'description': 'Return the sum of two numbers'
    }
    
    print("Problem:", problem['title'])
    print("Strategies available:")
    print("  - Zero-shot")
    print("  - Few-shot")
    print("  - Chain-of-thought")


if __name__ == '__main__':
    print("AI Model Evaluation Framework - Examples")
    print("")
    
    example_basic_usage()
    example_model_registry()
    example_configuration()
    example_evaluation_flow()
    example_prompting()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("=" * 50)
