"""
Test for AI Generated Solution
Task ID: HumanEval/62
Model: codellama:7b
"""

def derivative(xs):
    return [x*i for i, x in enumerate(xs, start=1)]



METADATA = {}


def check(candidate):
    assert candidate([3, 1, 2, 4, 5]) == [1, 4, 12, 20]
    assert candidate([1, 2, 3]) == [2, 6]
    assert candidate([3, 2, 1]) == [2, 2]
    assert candidate([3, 2, 1, 0, 4]) == [2, 2, 0, 16]
    assert candidate([1]) == []

