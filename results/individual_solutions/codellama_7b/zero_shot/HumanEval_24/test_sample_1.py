"""
Test for AI Generated Solution
Task ID: HumanEval/24
Model: codellama:7b
"""

def largest_divisor(n):
    for i in range(n-1, 0, -1):
        if n % i == 0:
            return i
    return 1



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate(3) == 1
    assert candidate(7) == 1
    assert candidate(10) == 5
    assert candidate(100) == 50
    assert candidate(49) == 7
