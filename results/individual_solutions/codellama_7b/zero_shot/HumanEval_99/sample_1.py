"""
AI Generated Solution
Task ID: HumanEval/99
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.264547
"""

def closest_integer(value):
    if value == "0":
        return 0
    elif abs(int(value)) < 1:
        return int(round(float(value), 2))
    else:
        return int(round(float(value)))

# Test cases
assert closest_integer("-14.5") == -15
assert closest_integer("14.5") == 15
assert closest_integer("0.5") == 1
assert closest_integer("-0.5") == -1
assert closest_integer("2.5") == 3
assert closest_integer("-2.5") == -3
assert closest_integer("10.8") == 11
assert closest_integer("-10.8") == -11
assert closest_integer("100.8") == 101
assert closest_integer("-100.8") == -101
assert closest_integer("0.04") == 0
assert closest_integer("-0.04") == 0
assert closest_integer("0.06") == 1
assert closest_integer("-0.06") == -1
assert closest_integer("123456789.123456") == 123456789
assert closest_integer("-123456789.123456") == -123456789
