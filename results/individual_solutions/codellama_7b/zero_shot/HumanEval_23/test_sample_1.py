"""
Test for AI Generated Solution
Task ID: HumanEval/23
Model: codellama:7b
"""

def strlen(my_string):
    return len(my_string)



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('') == 0
    assert candidate('x') == 1
    assert candidate('asdasnakj') == 9
