"""
Test for AI Generated Solution
Task ID: HumanEval/90
Model: codellama:7b
"""

def next_smallest(lst):
    if len(lst) < 2:
        return None
    sorted_lst = sorted(lst)
    for i in range(len(lst)):
        if sorted_lst[i+1] != sorted_lst[i]:
            return sorted_lst[i+1]
    return None

def check(candidate):

    # Check some simple cases
    assert candidate([1, 2, 3, 4, 5]) == 2
    assert candidate([5, 1, 4, 3, 2]) == 2
    assert candidate([]) == None
    assert candidate([1, 1]) == None
    assert candidate([1,1,1,1,0]) == 1
    assert candidate([1, 0**0]) == None
    assert candidate([-35, 34, 12, -45]) == -35

    # Check some edge cases that are easy to work out by hand.
    assert True

