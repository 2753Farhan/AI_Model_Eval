"""
Test for AI Generated Solution
Task ID: HumanEval/40
Model: codellama:7b
"""

def triples_sum_to_zero(my_list):
    for i in range(len(my_list)):
        for j in range(i+1, len(my_list)):
            for k in range(j+1, len(my_list)):
                if my_list[i] + my_list[j] + my_list[k] == 0:
                    return True
    return False



METADATA = {}


def check(candidate):
    assert candidate([1, 3, 5, 0]) == False
    assert candidate([1, 3, 5, -1]) == False
    assert candidate([1, 3, -2, 1]) == True
    assert candidate([1, 2, 3, 7]) == False
    assert candidate([1, 2, 5, 7]) == False
    assert candidate([2, 4, -5, 3, 9, 7]) == True
    assert candidate([1]) == False
    assert candidate([1, 3, 5, -100]) == False
    assert candidate([100, 3, 5, -100]) == False

