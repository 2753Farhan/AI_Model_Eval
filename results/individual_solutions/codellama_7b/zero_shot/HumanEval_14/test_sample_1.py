"""
Test for AI Generated Solution
Task ID: HumanEval/14
Model: codellama:7b
"""

def all_prefixes(string):
    return [string[:i] for i in range(1, len(string)+1)]



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('') == []
    assert candidate('asdfgh') == ['a', 'as', 'asd', 'asdf', 'asdfg', 'asdfgh']
    assert candidate('WWW') == ['W', 'WW', 'WWW']
