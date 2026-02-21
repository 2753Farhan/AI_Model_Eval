"""
Test for AI Generated Solution
Task ID: HumanEval/58
Model: codellama:7b
"""

def common(list1, list2):
    return sorted(set(list1).intersection(set(list2)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()



METADATA = {}


def check(candidate):
    assert candidate([1, 4, 3, 34, 653, 2, 5], [5, 7, 1, 5, 9, 653, 121]) == [1, 5, 653]
    assert candidate([5, 3, 2, 8], [3, 2]) == [2, 3]
    assert candidate([4, 3, 2, 8], [3, 2, 4]) == [2, 3, 4]
    assert candidate([4, 3, 2, 8], []) == []

