"""
AI Generated Solution
Task ID: HumanEval/76
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.231017
"""

def is_simple_power(x, n):
    if x == n**int(log(n, x)) and log(n, x) % 1 == 0:
        return True
    else:
        return False