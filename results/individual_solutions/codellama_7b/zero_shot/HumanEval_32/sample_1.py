"""
AI Generated Solution
Task ID: HumanEval/32
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.156326
"""

def find_zero(xs):
    if len(xs) % 2 == 1 or max(xs[::2]) <= 0:
        return None
    x0 = -1
    while abs(poly(xs, x0)) > 1e-6:
        x0 += 0.1
    return x0