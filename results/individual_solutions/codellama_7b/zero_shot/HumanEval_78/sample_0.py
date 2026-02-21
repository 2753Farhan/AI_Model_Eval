"""
AI Generated Solution
Task ID: HumanEval/78
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.233016
"""

def hex_key(num):
    count = 0
    for i in range(len(num)):
        if is_prime(int(num[i], 16)):
            count += 1
    return count

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True