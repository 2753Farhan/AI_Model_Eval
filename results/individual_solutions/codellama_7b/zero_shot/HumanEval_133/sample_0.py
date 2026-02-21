"""
AI Generated Solution
Task ID: HumanEval/133
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.309128
"""

def sum_squares(lst):
    result = 0
    for i in lst:
        result += int(round(i**2))
    return result