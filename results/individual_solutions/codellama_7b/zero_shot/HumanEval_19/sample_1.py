"""
AI Generated Solution
Task ID: HumanEval/19
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.126897
"""

def sort_numbers(numbers: str) -> str:
    number_list = numbers.split()
    sorted_numbers = sorted(number_list, key=lambda x: int(x))
    return ' '.join(sorted_numbers)