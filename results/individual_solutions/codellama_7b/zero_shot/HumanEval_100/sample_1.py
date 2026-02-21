"""
AI Generated Solution
Task ID: HumanEval/100
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.266547
"""

def make_a_pile(n):
    if n == 1:
        return [n]
    else:
        next_level = None
        if n % 2 == 0:
            next_level = n + 1
        else:
            next_level = n + 2
        return [n] + make_a_pile(next_level)