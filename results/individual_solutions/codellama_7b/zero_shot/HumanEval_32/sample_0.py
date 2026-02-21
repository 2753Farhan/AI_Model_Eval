"""
AI Generated Solution
Task ID: HumanEval/32
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.156326
"""

def find_zero(xs):
    if len(xs) % 2 == 1 or max(xs[::2]) <= 0:
        return None
    x0 = -max(xs[::2])
    while True:
        y = poly(xs, x0)
        if abs(y) < 1e-6:
            return x0
        x1 = x0 - y / poly(xs, x0)
        if abs(x1 - x0) < 1e-6:
            return x1
        x0 = x1