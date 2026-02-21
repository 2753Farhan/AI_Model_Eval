"""
AI Generated Solution
Task ID: HumanEval/39
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.168848
"""

def prime_fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
        if is_prime(a) == False:
            return prime_fib(i+1)
    return a

def is_prime(n):
    if n == 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True