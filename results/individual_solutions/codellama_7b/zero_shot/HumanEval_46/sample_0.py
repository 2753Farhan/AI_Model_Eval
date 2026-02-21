"""
AI Generated Solution
Task ID: HumanEval/46
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.180359
"""

def fib4(n):
    if n <= 3:
        return 0
    else:
        return fib4(n-1) + fib4(n-2) + fib4(n-3) + fib4(n-4)