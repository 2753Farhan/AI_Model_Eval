"""
Test for AI Generated Solution
Task ID: HumanEval/48
Model: codellama:7b
"""

def is_palindrome(text: str) -> bool:
    """
    Checks if given string is a palindrome

    Args:
        text (str): input string

    Returns:
        bool: True if the string is a palindrome, False otherwise
    """
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

