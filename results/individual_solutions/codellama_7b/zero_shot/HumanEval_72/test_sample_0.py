"""
Test for AI Generated Solution
Task ID: HumanEval/72
Model: codellama:7b
"""

def will_it_fly(q, w):
    if len(q) == 0:
        return False
    if q == q[::-1]:
        total = sum(q)
        if total <= w:
            return True
    return False

def check(candidate):

    # Check some simple cases
    assert candidate([3, 2, 3], 9) is True
    assert candidate([1, 2], 5) is False
    assert candidate([3], 5) is True
    assert candidate([3, 2, 3], 1) is False


    # Check some edge cases that are easy to work out by hand.
    assert candidate([1, 2, 3], 6) is False
    assert candidate([5], 5) is True

