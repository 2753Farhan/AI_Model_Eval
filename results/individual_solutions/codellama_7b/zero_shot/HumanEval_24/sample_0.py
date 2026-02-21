"""
AI Generated Solution
Task ID: HumanEval/24
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.139316
"""

def largest_divisor(n):
    for i in range(int(n**0.5), 0, -1):
        if n % i == 0:
            return i
    return 1