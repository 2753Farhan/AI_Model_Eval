"""
AI Generated Solution
Task ID: HumanEval/139
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.318640
"""

def special_factorial(n):
    if n <= 0:
        return 1
    else:
        return n * special_factorial(n-1)


# Test case 1:
assert special_factorial(4) == 288

# Test case 2:
assert special_factorial(5) == 120

# Test case 3:
assert special_factorial(6) == 720

# Test case 4:
assert special_factorial(7) == 5040

# Test case 5:
assert special_factorial(8) == 40320