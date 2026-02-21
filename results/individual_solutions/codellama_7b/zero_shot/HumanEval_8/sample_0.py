"""
AI Generated Solution
Task ID: HumanEval/8
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.098365
"""

def sum_product(numbers):
    if not numbers:
        return (0, 1)
    return (sum(numbers), reduce(lambda x, y: x * y, numbers))