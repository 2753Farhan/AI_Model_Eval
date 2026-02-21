"""
AI Generated Solution
Task ID: HumanEval/62
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.210984
"""

def derivative(xs):
    return [xs[i+1] * (i+1) for i in range(len(xs)-1)]