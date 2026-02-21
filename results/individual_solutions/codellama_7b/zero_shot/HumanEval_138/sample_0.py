"""
AI Generated Solution
Task ID: HumanEval/138
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.316646
"""

def is_equal_to_sum_even(n):
    for i in range(1, n+1):
        if i % 2 == 0:
            total = 0
            for j in range(1, 5):
                total += i
                if total == n:
                    return True
    return False