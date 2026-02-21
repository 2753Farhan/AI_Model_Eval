"""
Test for AI Generated Solution
Task ID: HumanEval/57
Model: codellama:7b
"""

def monotonic(my_list):
    if len(my_list) <= 1:
        return True
    elif my_list[0] < my_list[-1]:
        for i in range(len(my_list) - 1):
            if my_list[i] > my_list[i + 1]:
                return False
    else:
        for i in range(len(my_list) - 1):
            if my_list[i] < my_list[i + 1]:
                return False
    return True



METADATA = {}


def check(candidate):
    assert candidate([1, 2, 4, 10]) == True
    assert candidate([1, 2, 4, 20]) == True
    assert candidate([1, 20, 4, 10]) == False
    assert candidate([4, 1, 0, -10]) == True
    assert candidate([4, 1, 1, 0]) == True
    assert candidate([1, 2, 3, 2, 5, 60]) == False
    assert candidate([1, 2, 3, 4, 5, 60]) == True
    assert candidate([9, 9, 9, 9]) == True

