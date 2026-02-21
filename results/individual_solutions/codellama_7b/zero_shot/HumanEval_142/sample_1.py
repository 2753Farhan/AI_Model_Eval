"""
AI Generated Solution
Task ID: HumanEval/142
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.324158
"""

def sum_squares(lst):
    result = 0
    for i, x in enumerate(lst):
        if i % 3 == 0:
            result += x * x
        elif i % 4 == 0 and i % 3 != 0:
            result += x * x * x
    return result