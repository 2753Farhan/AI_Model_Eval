"""
AI Generated Solution
Task ID: HumanEval/10
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.104875
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