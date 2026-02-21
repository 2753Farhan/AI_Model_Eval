"""
AI Generated Solution
Task ID: HumanEval/80
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.236012
"""

def is_happy(s):
    if len(s) < 3:
        return False
    for i in range(len(s) - 2):
        if s[i] == s[i+1] and s[i+1] == s[i+2]:
            return False
    return True