"""
AI Generated Solution
Task ID: HumanEval/97
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.261548
"""

def multiply(a, b):
    product = a * b
    unit_digits = [int(digit) for digit in str(product)]
    result = sum(unit_digits)
    return result