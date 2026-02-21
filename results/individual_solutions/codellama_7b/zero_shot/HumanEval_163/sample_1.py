"""
AI Generated Solution
Task ID: HumanEval/163
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.353180
"""

def generate_integers(a, b):
    if a > b:
        return []
    else:
        return [x for x in range(a, b+1) if x % 2 == 0]