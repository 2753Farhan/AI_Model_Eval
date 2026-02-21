"""
AI Generated Solution
Task ID: HumanEval/13
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.114382
"""

def greatest_common_divisor(a, b):
    while b != 0:
        a, b = b, a % b
    return a