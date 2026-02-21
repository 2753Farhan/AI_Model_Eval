"""
AI Generated Solution
Task ID: HumanEval/24
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.140320
"""

def largest_divisor(n):
    for i in range(n-1, 0, -1):
        if n % i == 0:
            return i
    return 1