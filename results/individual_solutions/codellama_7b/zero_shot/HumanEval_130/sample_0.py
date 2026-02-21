"""
AI Generated Solution
Task ID: HumanEval/130
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.305129
"""

def tribonacci(n):
    if n == 0:
        return [1]
    elif n % 2 == 0:
        return [1, 3] + tribonacci(n-2)
    else:
        return [1, 3] + list(map(sum, zip(tribonacci(n-1), tribonacci(n-2))))