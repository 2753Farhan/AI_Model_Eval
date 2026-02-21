"""
AI Generated Solution
Task ID: HumanEval/21
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.131898
"""

def rescale_to_unit(numbers):
    if len(numbers) < 2:
        raise ValueError("List of numbers must have at least two elements.")
    smallest = min(numbers)
    largest = max(numbers)
    return [((n - smallest) / (largest - smallest)) for n in numbers]