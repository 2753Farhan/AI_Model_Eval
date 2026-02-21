"""
AI Generated Solution
Task ID: HumanEval/80
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.235016
"""

def is_happy(s):
    # Check if the length of the string is at least 3
    if len(s) < 3:
        return False

    # Check if every 3 consecutive letters are distinct
    for i in range(len(s) - 2):
        if s[i] == s[i+1] and s[i+1] == s[i+2]:
            return False

    return True