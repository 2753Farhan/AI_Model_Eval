"""
AI Generated Solution
Task ID: HumanEval/131
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.307129
"""

def digits(n):
    product = 1
    while n > 0:
        digit = n % 10
        if digit % 2 == 1:
            product *= digit
        n //= 10
    return product


# Test case 1:
assert digits(1) == 1
# Test case 2:
assert digits(4) == 0
# Test case 3:
assert digits(235) == 15