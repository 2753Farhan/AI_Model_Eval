"""
Test for AI Generated Solution
Task ID: HumanEval/13
Model: codellama:7b
"""

def greatest_common_divisor(a, b):
    while b != 0:
        a, b = b, a % b
    return a



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate(3, 7) == 1
    assert candidate(10, 15) == 5
    assert candidate(49, 14) == 7
    assert candidate(144, 60) == 12
