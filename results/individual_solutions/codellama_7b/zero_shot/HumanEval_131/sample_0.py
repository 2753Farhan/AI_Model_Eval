"""
AI Generated Solution
Task ID: HumanEval/131
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.306130
"""

def digits(n):
    product = 1
    while n > 0:
        digit = n % 10
        if digit % 2 == 1:
            product *= digit
        n //= 10
    return product

assert digits(1) == 1
assert digits(4) == 0
assert digits(235) == 15