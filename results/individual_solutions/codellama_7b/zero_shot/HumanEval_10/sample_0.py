"""
AI Generated Solution
Task ID: HumanEval/10
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.103869
"""

def is_palindrome(string):
    return string == string[::-1]


def make_palindrome(string):
    if is_palindrome(string):
        return string
    else:
        prefix = string[:len(string) // 2]
        suffix = string[len(string) // 2:]
        return prefix + suffix[::-1]