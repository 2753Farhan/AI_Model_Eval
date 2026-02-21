"""
AI Generated Solution
Task ID: HumanEval/112
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.280058
"""

def reverse_delete(s, c):
    # Remove all characters in s that are present in c
    for i in range(len(s) - 1, -1, -1):
        if s[i] in c:
            s = s[:i] + s[i+1:]

    # Check if the result string is a palindrome
    return (s, s == s[::-1])