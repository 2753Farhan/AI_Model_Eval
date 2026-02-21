"""
AI Generated Solution
Task ID: HumanEval/46
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.181359
"""

def fib4(n: int):
    if n <= 3:
        return 0
    else:
        a, b, c = 0, 2, 0
        for i in range(n-3):
            a, b, c = b, c, a+b+c
        return a+b+c