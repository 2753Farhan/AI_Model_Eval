"""
AI Generated Solution
Task ID: HumanEval/159
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.346187
"""

def eat(number, need, remaining):
    total = number + remaining
    if total >= need:
        return [total - need, 0]
    else:
        return [total, need - total]