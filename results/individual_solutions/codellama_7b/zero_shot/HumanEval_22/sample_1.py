"""
AI Generated Solution
Task ID: HumanEval/22
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.134920
"""

def filter_integers(values: List[Any]) -> List[int]:
    return [value for value in values if type(value) == int]