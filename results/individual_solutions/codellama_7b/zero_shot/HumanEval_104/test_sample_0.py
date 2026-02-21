"""
Test for AI Generated Solution
Task ID: HumanEval/104
Model: codellama:7b
"""

def unique_digits(x):
    result = []
    for num in x:
        if all([digit % 2 != 0 for digit in str(num)]):
            result.append(num)
    return sorted(result)

def check(candidate):

    # Check some simple cases
    assert candidate([15, 33, 1422, 1]) == [1, 15, 33]
    assert candidate([152, 323, 1422, 10]) == []
    assert candidate([12345, 2033, 111, 151]) == [111, 151]
    assert candidate([135, 103, 31]) == [31, 135]

    # Check some edge cases that are easy to work out by hand.
    assert True

