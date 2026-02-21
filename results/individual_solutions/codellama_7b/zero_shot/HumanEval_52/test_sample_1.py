"""
Test for AI Generated Solution
Task ID: HumanEval/52
Model: codellama:7b
"""

def below_threshold(my_list, threshold):
    for num in my_list:
        if num > threshold:
            return False
    return True



METADATA = {}


def check(candidate):
    assert candidate([1, 2, 4, 10], 100)
    assert not candidate([1, 20, 4, 10], 5)
    assert candidate([1, 20, 4, 10], 21)
    assert candidate([1, 20, 4, 10], 22)
    assert candidate([1, 8, 4, 10], 11)
    assert not candidate([1, 8, 4, 10], 10)

