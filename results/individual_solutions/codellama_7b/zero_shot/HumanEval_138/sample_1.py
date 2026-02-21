"""
AI Generated Solution
Task ID: HumanEval/138
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.317646
"""

def is_equal_to_sum_even(n):
    for i in range(1, n+1):
        if n == i*2:
            return True
    return False