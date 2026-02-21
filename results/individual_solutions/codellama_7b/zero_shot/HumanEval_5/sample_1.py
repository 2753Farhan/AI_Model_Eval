"""
AI Generated Solution
Task ID: HumanEval/5
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.090220
"""

def intersperse(numbers, delimeter):
    return [numbers[i] for i in range(len(numbers))] + [delimeter] * (len(numbers) - 1)