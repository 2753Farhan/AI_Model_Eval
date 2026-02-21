"""
Test for AI Generated Solution
Task ID: HumanEval/19
Model: codellama:7b
"""

def sort_numbers(numbers_str):
    numbers = [int(x) for x in numbers_str.split()]
    return " ".join([str(x) for x in sorted(numbers)])



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('') == ''
    assert candidate('three') == 'three'
    assert candidate('three five nine') == 'three five nine'
    assert candidate('five zero four seven nine eight') == 'zero four five seven eight nine'
    assert candidate('six five four three two one zero') == 'zero one two three four five six'
