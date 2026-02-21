"""
Test for AI Generated Solution
Task ID: HumanEval/9
Model: codellama:7b
"""

def rolling_max(numbers):
    max_val = []
    for i in range(len(numbers)):
        curr_max = max(numbers[:i+1])
        max_val.append(curr_max)
    return max_val



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([]) == []
    assert candidate([1, 2, 3, 4]) == [1, 2, 3, 4]
    assert candidate([4, 3, 2, 1]) == [4, 4, 4, 4]
    assert candidate([3, 2, 3, 100, 3]) == [3, 3, 3, 100, 100]
