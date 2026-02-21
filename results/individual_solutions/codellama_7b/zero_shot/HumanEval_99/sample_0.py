"""
AI Generated Solution
Task ID: HumanEval/99
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.263548
"""

def closest_integer(value):
    x = float(value)
    if x < 0:
        return int(x - 0.5)
    else:
        return int(x + 0.5)


# Test cases
assert closest_integer("10") == 10
assert closest_integer("15.3") == 15
assert closest_integer("-14.5") == -15
assert closest_integer("-14.2") == -14
assert closest_integer("-14.8") == -15
assert closest_integer("14.5") == 15
assert closest_integer("14.2") == 14
assert closest_integer("14.8") == 15