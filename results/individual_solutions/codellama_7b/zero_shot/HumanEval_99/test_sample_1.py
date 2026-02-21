"""
Test for AI Generated Solution
Task ID: HumanEval/99
Model: codellama:7b
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


def check(candidate):

    # Check some simple cases
    assert candidate("10") == 10, "Test 1"
    assert candidate("14.5") == 15, "Test 2"
    assert candidate("-15.5") == -16, "Test 3"
    assert candidate("15.3") == 15, "Test 3"

    # Check some edge cases that are easy to work out by hand.
    assert candidate("0") == 0, "Test 0"

