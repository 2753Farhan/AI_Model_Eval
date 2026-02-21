"""
Test for AI Generated Solution
Task ID: HumanEval/47
Model: codellama:7b
"""

def median(my_list):
    sorted_list = sorted(my_list)
    length = len(sorted_list)
    if length % 2 == 0:
        # even number of elements
        median1 = sorted_list[length // 2]
        median2 = sorted_list[length // 2 - 1]
        return (median1 + median2) / 2
    else:
        # odd number of elements
        return sorted_list[length // 2]



METADATA = {}


def check(candidate):
    assert candidate([3, 1, 2, 4, 5]) == 3
    assert candidate([-10, 4, 6, 1000, 10, 20]) == 8.0
    assert candidate([5]) == 5
    assert candidate([6, 5]) == 5.5
    assert candidate([8, 1, 3, 9, 9, 2, 7]) == 7 

