"""
Test for AI Generated Solution
Task ID: HumanEval/12
Model: codellama:7b
"""

def longest(strings):
    if not strings:
        return None
    return max(strings, key=len)


# Test cases:
print(longest([]) == None)  # True
print(longest(['a', 'b', 'c']) == 'a')  # True
print(longest(['a', 'bb', 'ccc']) == 'ccc')  # True



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([]) == None
    assert candidate(['x', 'y', 'z']) == 'x'
    assert candidate(['x', 'yyy', 'zzzz', 'www', 'kkkk', 'abc']) == 'zzzz'
