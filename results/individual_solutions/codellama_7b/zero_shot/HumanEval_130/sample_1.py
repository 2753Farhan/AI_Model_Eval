"""
AI Generated Solution
Task ID: HumanEval/130
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.305129
"""

def tribonacci(n):
    if n == 0:
        return [1]
    elif n % 2 == 0:
        return [1, 3, 2] + tribonacci(n-3)
    else:
        return [1] + tribonacci(n-1) + [1]