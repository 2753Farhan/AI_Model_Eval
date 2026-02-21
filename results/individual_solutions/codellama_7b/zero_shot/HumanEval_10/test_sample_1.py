"""
Test for AI Generated Solution
Task ID: HumanEval/10
Model: codellama:7b
"""

def is_palindrome(string):
    return string == string[::-1]

def make_palindrome(string):
    if is_palindrome(string):
        return string
    else:
        palindromic_suffix = ""
        for i in range(len(string)):
            if is_palindrome(string[i:]):
                palindromic_suffix = string[i:]
                break
        return string + palindromic_suffix[::-1]



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('') == ''
    assert candidate('x') == 'x'
    assert candidate('xyz') == 'xyzyx'
    assert candidate('xyx') == 'xyx'
    assert candidate('jerry') == 'jerryrrej'
