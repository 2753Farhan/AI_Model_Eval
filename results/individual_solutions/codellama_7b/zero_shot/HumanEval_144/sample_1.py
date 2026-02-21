"""
AI Generated Solution
Task ID: HumanEval/144
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.326159
"""

def simplify(x, n):
    x_numerator, x_denominator = x.split("/")
    n_numerator, n_denominator = n.split("/")
    result = int(x_numerator) * int(n_numerator)
    if result % int(n_denominator) == 0:
        return True
    else:
        return False