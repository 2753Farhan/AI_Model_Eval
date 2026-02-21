"""
Test for AI Generated Solution
Task ID: HumanEval/99
Model: codellama:7b
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

def check(candidate):

    # Check some simple cases
    assert candidate("10") == 10, "Test 1"
    assert candidate("14.5") == 15, "Test 2"
    assert candidate("-15.5") == -16, "Test 3"
    assert candidate("15.3") == 15, "Test 3"

    # Check some edge cases that are easy to work out by hand.
    assert candidate("0") == 0, "Test 0"

