"""
AI Generated Solution
Task ID: HumanEval/19
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.126897
"""

def sort_numbers(numbers_str):
    numbers = [int(x) for x in numbers_str.split()]
    return " ".join([str(x) for x in sorted(numbers)])