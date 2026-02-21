"""
Test for AI Generated Solution
Task ID: HumanEval/34
Model: codellama:7b
"""

def unique(my_list):
    return list(dict.fromkeys(my_list))



METADATA = {}


def check(candidate):
    assert candidate([5, 3, 5, 2, 3, 3, 9, 0, 123]) == [0, 2, 3, 5, 9, 123]

