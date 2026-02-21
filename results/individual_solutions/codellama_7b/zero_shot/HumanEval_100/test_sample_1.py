"""
Test for AI Generated Solution
Task ID: HumanEval/100
Model: codellama:7b
"""

def make_a_pile(n):
    if n == 1:
        return [n]
    else:
        next_level = None
        if n % 2 == 0:
            next_level = n + 1
        else:
            next_level = n + 2
        return [n] + make_a_pile(next_level)

def check(candidate):

    # Check some simple cases
    assert candidate(3) == [3, 5, 7], "Test 3"
    assert candidate(4) == [4,6,8,10], "Test 4"
    assert candidate(5) == [5, 7, 9, 11, 13]
    assert candidate(6) == [6, 8, 10, 12, 14, 16]
    assert candidate(8) == [8, 10, 12, 14, 16, 18, 20, 22]

    # Check some edge cases that are easy to work out by hand.
    assert True, "This prints if this assert fails 2 (also good for debugging!)"

