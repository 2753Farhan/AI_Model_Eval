"""
AI Generated Solution
Task ID: HumanEval/106
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.273059
"""

def f(n):
    result = []
    for i in range(1, n+1):
        if i % 2 == 0:
            result.append(factorial(i))
        else:
            result.append(sum(range(1, i+1)))
    return result

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)