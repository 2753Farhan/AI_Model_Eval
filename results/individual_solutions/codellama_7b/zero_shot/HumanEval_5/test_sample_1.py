"""
Test for AI Generated Solution
Task ID: HumanEval/5
Model: codellama:7b
"""

def intersperse(numbers, delimeter):
    return [numbers[i] for i in range(len(numbers))] + [delimeter] * (len(numbers) - 1)



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([], 7) == []
    assert candidate([5, 6, 3, 2], 8) == [5, 8, 6, 8, 3, 8, 2]
    assert candidate([2, 2, 2], 2) == [2, 2, 2, 2, 2]
