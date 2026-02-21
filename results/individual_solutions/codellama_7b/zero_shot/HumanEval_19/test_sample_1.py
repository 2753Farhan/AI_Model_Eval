"""
Test for AI Generated Solution
Task ID: HumanEval/19
Model: codellama:7b
"""

def sort_numbers(numbers: str) -> str:
    number_list = numbers.split()
    sorted_numbers = sorted(number_list, key=lambda x: int(x))
    return ' '.join(sorted_numbers)



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
