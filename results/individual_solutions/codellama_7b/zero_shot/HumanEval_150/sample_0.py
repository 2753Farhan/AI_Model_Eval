"""
AI Generated Solution
Task ID: HumanEval/150
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.333663
"""

def x_or_y(n, x, y):
    if is_prime(n):
        return x
    else:
        return y


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True