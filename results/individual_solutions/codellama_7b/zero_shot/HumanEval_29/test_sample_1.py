"""
Test for AI Generated Solution
Task ID: HumanEval/29
Model: codellama:7b
"""

def filter_by_prefix(strings, prefix):
    return [string for string in strings if string.startswith(prefix)]



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([], 'john') == []
    assert candidate(['xxx', 'asd', 'xxy', 'john doe', 'xxxAAA', 'xxx'], 'xxx') == ['xxx', 'xxxAAA', 'xxx']
