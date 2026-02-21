"""
AI Generated Solution
Task ID: HumanEval/55
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.197462
"""

def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)