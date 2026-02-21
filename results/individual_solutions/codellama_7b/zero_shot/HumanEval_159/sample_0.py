"""
AI Generated Solution
Task ID: HumanEval/159
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.346187
"""

def eat(number, need, remaining):
    total = number + need
    if total > remaining:
        return [remaining, 0]
    else:
        return [total, remaining - total]