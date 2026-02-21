"""
Test for AI Generated Solution
Task ID: HumanEval/28
Model: codellama:7b
"""

def concatenate(strings):
    return "".join(strings)



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([]) == ''
    assert candidate(['x', 'y', 'z']) == 'xyz'
    assert candidate(['x', 'y', 'z', 'w', 'k']) == 'xyzwk'
