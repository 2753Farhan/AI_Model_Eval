"""
Test for AI Generated Solution
Task ID: HumanEval/127
Model: codellama:7b
"""

def intersection(interval1, interval2):
    if not (interval1[0] <= interval2[1] and interval2[0] <= interval1[1]):
        return "NO"

    start = max(interval1[0], interval2[0])
    end = min(interval1[1], interval2[1])

    if start > end:
        return "NO"

    prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    for prime in prime_numbers:
        if start < end and (end - start) == prime:
            return "YES"

    return "NO"

def check(candidate):

    # Check some simple cases
    assert candidate((1, 2), (2, 3)) == "NO"
    assert candidate((-1, 1), (0, 4)) == "NO"
    assert candidate((-3, -1), (-5, 5)) == "YES"
    assert candidate((-2, 2), (-4, 0)) == "YES"

    # Check some edge cases that are easy to work out by hand.
    assert candidate((-11, 2), (-1, -1)) == "NO"
    assert candidate((1, 2), (3, 5)) == "NO"
    assert candidate((1, 2), (1, 2)) == "NO"
    assert candidate((-2, -2), (-3, -2)) == "NO"

