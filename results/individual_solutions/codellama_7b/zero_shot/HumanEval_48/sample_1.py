"""
AI Generated Solution
Task ID: HumanEval/48
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.184359
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
