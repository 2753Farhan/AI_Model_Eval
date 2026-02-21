"""
AI Generated Solution
Task ID: HumanEval/96
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.260542
"""

def count_up_to(n):
    if n < 0:
        return []
    prime_numbers = []
    for i in range(2, n+1):
        if all(i % num != 0 for num in range(2, int(i ** 0.5) + 1)):
            prime_numbers.append(i)
    return prime_numbers