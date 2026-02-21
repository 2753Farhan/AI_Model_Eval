"""
Test for AI Generated Solution
Task ID: HumanEval/42
Model: codellama:7b
"""

def incr_list(my_list):
    return [x+1 for x in my_list]



METADATA = {}


def check(candidate):
    assert candidate([]) == []
    assert candidate([3, 2, 1]) == [4, 3, 2]
    assert candidate([5, 2, 5, 2, 3, 3, 9, 0, 123]) == [6, 3, 6, 3, 4, 4, 10, 1, 124]

