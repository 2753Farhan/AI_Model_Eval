"""
Test for AI Generated Solution
Task ID: HumanEval/128
Model: codellama:7b
"""

def prod_signs(arr):
    if not arr:
        return None
    product = 1
    for num in arr:
        sign = 1 if num > 0 else -1 if num < 0 else 0
        product *= sign
    return product * sum(abs(num) for num in arr)

def check(candidate):

    # Check some simple cases
    assert True, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate([1, 2, 2, -4]) == -9
    assert candidate([0, 1]) == 0
    assert candidate([1, 1, 1, 2, 3, -1, 1]) == -10
    assert candidate([]) == None
    assert candidate([2, 4,1, 2, -1, -1, 9]) == 20
    assert candidate([-1, 1, -1, 1]) == 4
    assert candidate([-1, 1, 1, 1]) == -4
    assert candidate([-1, 1, 1, 0]) == 0

    # Check some edge cases that are easy to work out by hand.
    assert True, "This prints if this assert fails 2 (also good for debugging!)"

