"""
AI Generated Solution
Task ID: HumanEval/75
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.229006
"""

def is_multiply_prime(a):
    if a >= 100:
        return False
    for i in range(2, int(a ** 0.5) + 1):
        if a % i == 0:
            return False
    return True