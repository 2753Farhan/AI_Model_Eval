"""
Test for AI Generated Solution
Task ID: HumanEval/22
Model: codellama:7b
"""

def filter_integers(values: List[Any]) -> List[int]:
    return [value for value in values if type(value) == int]



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([]) == []
    assert candidate([4, {}, [], 23.2, 9, 'adasd']) == [4, 9]
    assert candidate([3, 'c', 3, 3, 'a', 'b']) == [3, 3, 3]
