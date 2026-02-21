"""
AI Generated Solution
Task ID: HumanEval/64
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.213984
"""

def vowels_count(s):
    count = 0
    for i in range(len(s)):
        if s[i].lower() in ['a', 'e', 'i', 'o', 'u'] or (s[i].lower() == 'y' and i == len(s) - 1):
            count += 1
    return count