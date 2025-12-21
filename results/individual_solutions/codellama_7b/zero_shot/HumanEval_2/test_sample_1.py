"""
Test for AI Generated Solution
Task ID: HumanEval/2
Model: codellama:7b
"""

def truncate_number(number):
    return abs(number - int(number))



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate(3.5) == 0.5
    assert abs(candidate(1.33) - 0.33) < 1e-6
    assert abs(candidate(123.456) - 0.456) < 1e-6
