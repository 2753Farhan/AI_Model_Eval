"""
Test for AI Generated Solution
Task ID: HumanEval/48
Model: codellama:7b
"""

def is_palindrome(text):
    return text == text[::-1]



METADATA = {}


def check(candidate):
    assert candidate('') == True
    assert candidate('aba') == True
    assert candidate('aaaaa') == True
    assert candidate('zbcd') == False
    assert candidate('xywyx') == True
    assert candidate('xywyz') == False
    assert candidate('xywzx') == False

