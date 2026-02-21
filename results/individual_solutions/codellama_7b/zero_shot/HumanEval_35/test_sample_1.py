"""
Test for AI Generated Solution
Task ID: HumanEval/35
Model: codellama:7b
"""

def max_element(my_list):
    return max(my_list)



METADATA = {}


def check(candidate):
    assert candidate([1, 2, 3]) == 3
    assert candidate([5, 3, -5, 2, -3, 3, 9, 0, 124, 1, -10]) == 124
