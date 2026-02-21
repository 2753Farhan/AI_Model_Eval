"""
Test for AI Generated Solution
Task ID: HumanEval/136
Model: codellama:7b
"""

def largest_smallest_integers(lst):
    smallest_positive = None
    largest_negative = None

    for i in lst:
        if i > 0 and (smallest_positive is None or i < smallest_positive):
            smallest_positive = i
        elif i < 0 and (largest_negative is None or i > largest_negative):
            largest_negative = i

    return (largest_negative, smallest_positive)

def check(candidate):

    # Check some simple cases
    assert candidate([2, 4, 1, 3, 5, 7]) == (None, 1)
    assert candidate([2, 4, 1, 3, 5, 7, 0]) == (None, 1)
    assert candidate([1, 3, 2, 4, 5, 6, -2]) == (-2, 1)
    assert candidate([4, 5, 3, 6, 2, 7, -7]) == (-7, 2)
    assert candidate([7, 3, 8, 4, 9, 2, 5, -9]) == (-9, 2)
    assert candidate([]) == (None, None)
    assert candidate([0]) == (None, None)
    assert candidate([-1, -3, -5, -6]) == (-1, None)
    assert candidate([-1, -3, -5, -6, 0]) == (-1, None)
    assert candidate([-6, -4, -4, -3, 1]) == (-3, 1)
    assert candidate([-6, -4, -4, -3, -100, 1]) == (-3, 1)

    # Check some edge cases that are easy to work out by hand.
    assert True
