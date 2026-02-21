"""
AI Generated Solution
Task ID: HumanEval/72
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.224496
"""

def will_it_fly(q, w):
    if len(q) == 0:
        return False
    if q == q[::-1]:
        total = sum(q)
        if total <= w:
            return True
    return False