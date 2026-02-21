"""
AI Generated Solution
Task ID: HumanEval/5
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.090220
"""

def intersperse(numbers, delimeter):
    return [x for x in (delimeter if i % 2 == 0 else y for i, y in enumerate(numbers))][1:]