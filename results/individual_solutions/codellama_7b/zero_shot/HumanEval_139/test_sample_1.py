"""
Test for AI Generated Solution
Task ID: HumanEval/139
Model: codellama:7b
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

def check(candidate):

    # Check some simple cases
    assert candidate(4) == 288, "Test 4"
    assert candidate(5) == 34560, "Test 5"
    assert candidate(7) == 125411328000, "Test 7"

    # Check some edge cases that are easy to work out by hand.
    assert candidate(1) == 1, "Test 1"

