"""
AI Generated Solution
Task ID: HumanEval/139
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.318640
"""

def special_factorial(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result