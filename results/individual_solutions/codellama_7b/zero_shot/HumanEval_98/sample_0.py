"""
AI Generated Solution
Task ID: HumanEval/98
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.262548
"""

def count_upper(s):
    count = 0
    for i in range(len(s)):
        if i % 2 == 0 and s[i].isupper() and s[i] in 'AEIOU':
            count += 1
    return count