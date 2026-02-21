"""
AI Generated Solution
Task ID: HumanEval/59
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.204467
"""

def largest_prime_factor(n):
    if n <= 1 or is_prime(n):
        return n
    for i in range(int(n**0.5), 1, -1):
        if n % i == 0 and is_prime(i):
            return i
    return 1

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True