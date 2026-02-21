"""
Test for AI Generated Solution
Task ID: HumanEval/16
Model: codellama:7b
"""

def count_distinct_characters(string):
    return len(set(string.lower()))



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('') == 0
    assert candidate('abcde') == 5
    assert candidate('abcde' + 'cade' + 'CADE') == 5
    assert candidate('aaaaAAAAaaaa') == 1
    assert candidate('Jerry jERRY JeRRRY') == 5
