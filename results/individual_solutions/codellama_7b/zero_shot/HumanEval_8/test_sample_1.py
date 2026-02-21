"""
Test for AI Generated Solution
Task ID: HumanEval/8
Model: codellama:7b
"""

def sum_product(numbers):
    if not numbers:
        return (0, 1)
    return (sum(numbers), reduce(lambda x, y: x * y, numbers))



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([]) == (0, 1)
    assert candidate([1, 1, 1]) == (3, 1)
    assert candidate([100, 0]) == (100, 0)
    assert candidate([3, 5, 7]) == (3 + 5 + 7, 3 * 5 * 7)
    assert candidate([10]) == (10, 10)
