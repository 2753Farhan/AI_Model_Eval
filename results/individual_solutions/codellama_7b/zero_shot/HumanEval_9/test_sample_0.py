"""
Test for AI Generated Solution
Task ID: HumanEval/9
Model: codellama:7b
"""

def rolling_max(numbers):
    max_so_far = numbers[0]
    max_ending_here = numbers[0]
    result = []
    for i in range(len(numbers)):
        max_ending_here = max(max_ending_here, numbers[i])
        result.append(max_ending_here)
        if max_so_far < max_ending_here:
            max_so_far = max_ending_here
    return result



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([]) == []
    assert candidate([1, 2, 3, 4]) == [1, 2, 3, 4]
    assert candidate([4, 3, 2, 1]) == [4, 4, 4, 4]
    assert candidate([3, 2, 3, 100, 3]) == [3, 3, 3, 100, 100]
